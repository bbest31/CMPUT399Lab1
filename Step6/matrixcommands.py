#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from ev3dev.ev3 import *
from math import *
import threading

# ---------------------------------
# Global constants for this file.

# In seconds
timeDelta = 0.02
# In meters
wheelDiameter = 5.5/100
# In meters
wheelCircumference = 17.3/100
# In meters
vehicleWidth = 10.7/100
file = open("dead_reckoning_output", "w")

# Motors
motorLeft = LargeMotor(OUTPUT_B)
motorRight = LargeMotor(OUTPUT_C)


# -------------------------------

# Connect gyro
gy = GyroSensor()

# Put the gyro sensor into ANGLE mode.
gy.mode = 'GYRO-ANG'


assert motorRight.connected
assert motorLeft.connected


###########
# Functions for measurement
# These functions will run in their own thread.
###########


# currentTachoReading: int. Degrees of rotation per second for a wheel in the current measurement.
# previousTachoReading: int. Degrees of rotation per second for a wheel in the previous measurement.
# returns: float. Speed of the wheel in m/s
def wheelVelocity(currentTachoReading, previousTachoReading):
    return (wheelDiameter/2)*((currentTachoReading - previousTachoReading)/timeDelta)*((2*pi)/360)


# currentTachoReadingLeft: int. Degrees of rotation  per second for left wheel in the current measurement.
# previousTachoReadingLeft: int. Degrees of rotation per second of left wheel  in the previous measurement.
# currentTachoReadingLeft: int. Degrees of rotation  per second for right wheel in the current measurement.
# previousTachoReadingLeft: int. Degrees of rotation per second of right wheel  in the previous measurement.
# returns: float. Angular speed velocity of vehicle, in radians/sec
def angularVelocity(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight):
    return (wheelVelocity(currentTachoReadingRight, previousTachoReadingRight) - wheelVelocity(currentTachoReadingLeft, previousTachoReadingLeft))/vehicleWidth


# currentTachoReadingLeft: int. Degrees of rotation  per second for left wheel in the current measurement.
# previousTachoReadingLeft: int. Degrees of rotation per second of left wheel  in the previous measurement.
# currentTachoReadingLeft: int. Degrees of rotation  per second for right wheel in the current measurement.
# previousTachoReadingLeft: int. Degrees of rotation per second of right wheel  in the previous measurement.
# returns: float. Speed of the vehicle, essentially, an average for the speeds of the two wheels. in m/s
def vehicleVelocity(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight):
    return (wheelVelocity(currentTachoReadingRight, previousTachoReadingRight) + wheelVelocity(currentTachoReadingLeft, previousTachoReadingLeft))/2


# currentTachoReadingLeft: int. Degrees of rotation  per second for left wheel in the current measurement.
# previousTachoReadingLeft: int. Degrees of rotation per second of left wheel  in the previous measurement.
# currentTachoReadingLeft: int. Degrees of rotation  per second for right wheel in the current measurement.
# previousTachoReadingLeft: int. Degrees of rotation per second of right wheel  in the previous measurement.
# returns: float. The radius of a circle centered in the ICC of the vehicle in meters
# TODO what happens angularVelocity is 0? (vehicle is moving in a straight line and both wheels at the same speed) should this be 0?
#     according to http://www.cs.columbia.edu/~allen/F15/NOTES/icckinematics.pdf (page 2) it should be infinite. What do you think?
def radiusOfRotation(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight):
    return vehicleVelocity(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight)/angularVelociy(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight)

# angularVelocityTimeSeries: list<float>. Contains the discrete measurements for the angular velocity from 0 to (len(angularVelocityTimeSeries)-1)*deltaTime seconds
# returns: float. angle of rotation in radians


def theta(angularVelocityTimeSeries):
    # This is an approximation of an integral by using a Riemann sum
    theta = 0
    for measurement in angularVelocityTimeSeries:
        theta = theta + measurement
    return theta*timeDelta

# angularVelocityTimeSeries: list<float>. Contains the discrete measurements for the angular velocity from 0 to (len(angularVelocityTimeSeries)-1)*deltaTime seconds
# velocityTimeSeries: list<float>. Contains the discrete measurements for the linear velocity from 0 to (len(velocityTimeSeries)-1)*deltaTime seconds
# returns: float. the x coordinate measured from the point of origin. In meters.


def positionX(velocityTimeSeries, angularVelocityTimeSeries):
    # This is an approximation of an integral by using a Riemann sum
    x = 0
    for velocityMeasurement in velocityTimeSeries:
        x = x + velocityMeasurement
    x = x * cos(theta(angularVelocityTimeSeries))
    return x*timeDelta

# angularVelocityTimeSeries: list<float>. Contains the discrete measurements for the angular velocity from 0 to (len(angularVelocityTimeSeries)-1)*deltaTime seconds
# velocityTimeSeries: list<float>. Contains the discrete measurements for the linear velocity from 0 to (len(velocityTimeSeries)-1)*deltaTime seconds
# returns: float. the x coordinate measured from the point of origin. In meters.


def positionY(velocityTimeSeries, angularVelocityTimeSeries):
    # This is an approximation of an integral by using a Riemann sum
    x = 0
    for velocityMeasurement in velocityTimeSeries:
        x = x + velocityMeasurement
    x = x * sin(theta(angularVelocityTimeSeries))
    return x*timeDelta


# Store every single measurement of the angular velocity
wTimeSeries = []
# Store every single measurement of the velocity
vTimeseries = []




###########
# End of Functions for measurement
###########


pos = [0, 0]

Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

# commands correspond to [left-motor-speed, right-motor-speed, time duration (s)]
#commands = [[80, 60, 2], [60, 60, 1], [-50, 80, 2]]
commands = [[20,40,2]]

# Start measurement thread. This is a daemon thread which will terminate once
# The main program terminates.
#measuringThread = threading.Thread(target=measure, daemon=True)
#measuringThread.start()


totalTimeForCommands = 0

for command in commands:
    totalTimeForCommands = totalTimeForCommands + command[2]
runTime = 0

#Selects the relevant command based on the runtime
def selectCommand(runTime):
    timeSummation = 0
    for command in commands:
        if (runTime <= timeSummation):
            return command
        else:
            timeSummation = timeSummation + command[2]



# Run the commands given in the variable
# TODO instead of multithreading we could also consider refreshing this loop
#     every timeDelta seconds, and then figuring out when enough seconds have passed
#     so that we can move to the next instruction.
currentTachoReadingLeft = motorLeft.position
currentTachoReadingRight = motorRight.position
command = commands[0]
leftSpeed = (command[0]*0.01)*900
rightSpeed = (command[1]*0.01)*900
motorRight.run_timed(speed_sp=rightSpeed, time_sp=command[2]*1000)
motorLeft.run_timed(speed_sp=leftSpeed, time_sp=command[2]*1000)
posX=0
posY=0
angle=0
while (runTime <= 4):

    previousTachoReadingLeft = currentTachoReadingLeft
    previousTachoReadingRight = currentTachoReadingRight
    sleep(timeDelta)
    runTime = runTime+timeDelta
    currentTachoReadingLeft = motorLeft.position
    currentTachoReadingRight = motorRight.position
    
    wTimeSeries.append(angularVelocity(currentTachoReadingLeft, previousTachoReadingLeft,
                                           currentTachoReadingRight, previousTachoReadingRight))
    vTimeseries.append(vehicleVelocity(currentTachoReadingLeft, previousTachoReadingLeft,
                                           currentTachoReadingRight, previousTachoReadingRight))


angle = angle + theta(wTimeSeries)
posX = posX + positionX(vTimeseries, wTimeSeries)
posY = posY + positionY(vTimeseries, wTimeSeries)

file.write("--------------------------------\n")
file.write("Theta1(t): " + str(angle) + "\n")
file.write("PosX1(t): " + str(posX)+"\n")
file.write("PosY1(t): " + str(posY)+"\n")
motorRight.stop()
motorLeft.stop()

file.close()
