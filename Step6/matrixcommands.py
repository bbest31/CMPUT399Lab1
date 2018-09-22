#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from ev3dev.ev3 import *
from math import *
import threading

#---------------------------------
#Global constants for this file.

#In miliseconds 
timeDelta = 500/1000
#In meters
wheelDiameter=5.5/100
#In meters
wheelCircumference = 17.3/100
#In meters
vehicleWidth = 14.5/100

#Motors
motorLeft = LargeMotor(OUTPUT_B)
motorRight = LargeMotor(OUTPUT_C)


#-------------------------------

# Connect gyro
gy = GyroSensor() 

# Put the gyro sensor into ANGLE mode.
gy.mode='GYRO-ANG'


assert motorRight.connected
assert motorLeft.connected



###########
# Functions for measurement
# These functions will run in their own thread.
###########


#currentTachoReading: int. Degrees of rotation per second for a wheel in the current measurement.
#previousTachoReading: int. Degrees of rotation per second for a wheel in the previous measurement.
#returns: float. Speed of the wheel in m/s
def wheelVelocity(currentTachoReading, previousTachoReading):
    return (wheelDiameter/2)*((currentTachoReading - previousTachoReading)/timeDelta)*((2*pi)/360)


#currentTachoReadingLeft: int. Degrees of rotation  per second for left wheel in the current measurement.
#previousTachoReadingLeft: int. Degrees of rotation per second of left wheel  in the previous measurement.
#currentTachoReadingLeft: int. Degrees of rotation  per second for right wheel in the current measurement.
#previousTachoReadingLeft: int. Degrees of rotation per second of right wheel  in the previous measurement.
#returns: float. Angular speed velocity of vehicle, in radians/sec
def angularVelociy(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight):
    return (wheelVelocity(currentTachoReadingRight, previousTachoReadingRight) - wheelVelocity(currentTachoReadingLeft, previousTachoReadingLeft))/vehicleWidth


#currentTachoReadingLeft: int. Degrees of rotation  per second for left wheel in the current measurement.
#previousTachoReadingLeft: int. Degrees of rotation per second of left wheel  in the previous measurement.
#currentTachoReadingLeft: int. Degrees of rotation  per second for right wheel in the current measurement.
#previousTachoReadingLeft: int. Degrees of rotation per second of right wheel  in the previous measurement.
#returns: float. Speed of the vehicle, essentially, an average for the speeds of the two wheels. in m/s
def vehicleVelocity(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight):
    print("RIGHT VEL" + str(wheelVelocity(currentTachoReadingRight, previousTachoReadingRight)))
    print("LEFT VEL" + str(wheelVelocity(currentTachoReadingLeft, previousTachoReadingLeft)))
    return (wheelVelocity(currentTachoReadingRight, previousTachoReadingRight) + wheelVelocity(currentTachoReadingLeft, previousTachoReadingLeft))/2


#currentTachoReadingLeft: int. Degrees of rotation  per second for left wheel in the current measurement.
#previousTachoReadingLeft: int. Degrees of rotation per second of left wheel  in the previous measurement.
#currentTachoReadingLeft: int. Degrees of rotation  per second for right wheel in the current measurement.
#previousTachoReadingLeft: int. Degrees of rotation per second of right wheel  in the previous measurement.
#returns: float. The radius of a circle centered in the ICC of the vehicle in meters
#TODO what happens angularVelocity is 0? (vehicle is moving in a straight line and both wheels at the same speed) should this be 0?
#     according to http://www.cs.columbia.edu/~allen/F15/NOTES/icckinematics.pdf (page 2) it should be infinite. What do you think?
def radiusOfRotation(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight):
    return vehicleVelocity(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight)/angularVelociy(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight)
    


def measure():
    previousTachoReadingLeft = motorLeft.position
    previousTachoReadingRight = motorRight.position
    while True:
        #Gather measurements every timeDelta seconds
        sleep(timeDelta)
        currentTachoReadingLeft = motorLeft.position
        currentTachoReadingRight = motorRight.position
        #screen_lock.acquire()
        print("LEFT PREV TACHO: " + str(previousTachoReadingLeft) + " CURRENT TACHO: " + str(currentTachoReadingLeft))
        print(str(angularVelociy(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight)))
        print("RADIUS OF ROTATION: " + str(radiusOfRotation(currentTachoReadingLeft, previousTachoReadingLeft, currentTachoReadingRight, previousTachoReadingRight)))
        #screen_lock.release()
        #After all measurements are taken: 
        previousTachoReadingLeft = currentTachoReadingLeft
        previousTachoReadingRight = currentTachoReadingRight

###########
# End of Functions for measurement
###########

pos = [0,0]

Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

# commands correspond to [left-motor-speed, right-motor-speed, time duration (s)]
# commands = [[80,60,2],[60,60,1],[-50,80,2]]
commands = [[50,50,10]]

#Start measurement thread. This is a daemon thread which will terminate once 
#The main program terminates.
measuringThread = threading.Thread(target=measure,daemon=True)
measuringThread.start()


# Run the commands given in the variable
for command in commands:
    runTime = command[2]*1000
    leftSpeed = (command[0]*0.01)*900
    rightSpeed = (command[1]*0.01)*900
    currentAngle = gy.value()
    motorLeft.run_timed(time_sp=runTime, speed_sp=leftSpeed)
    motorRight.run_timed(time_sp=runTime, speed_sp=rightSpeed)
    sleep(command[2]+1)

