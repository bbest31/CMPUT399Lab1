#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make robot move in a straight line

from time import sleep
from ev3dev.ev3 import *
from math import *


motorRight = LargeMotor(OUTPUT_C)
motorLeft = LargeMotor(OUTPUT_B)

# Connect gyro
gy = GyroSensor()

# Put the gyro sensor into ANGLE mode.
gy.mode = 'GYRO-ANG'

#-------------------------
#Constants

#In meters
wheelDiameter = 5.5/100

#Wheel circumference in meters
wheelCircumference = wheelDiameter*pi

#-------------------------

assert motorRight.connected
assert motorLeft.connected

Leds.set_color(Leds.LEFT,  Leds.ORANGE)
sleep(0.5)

def wheelVelocity(degreesPerSecond):
    return ((wheelCircumference)*(degreesPerSecond/360))


#distance:float. Distance that we want the robot to travel in meters (must be positive)
#degreesPerSecond:integer. (Optional Parameter) the degrees per second the wheels are supposed to rotate
#returns: float. The error, defined by the actual distance (according to the enconders)
#                and the expected distance
def straightLineError(distance, degreesPerSecond=180):
    #In seconds
    timeOfMovement = (distance/wheelVelocity(degreesPerSecond))
    #Sensor Data
    #Current reading of the tachometer of each wheel  (in degrees)
    startingTachoReadingLeft = motorLeft.position
    startingTachoReadingRight = motorRight.position

    motorRight.run_timed(time_sp=timeOfMovement * 1000, speed_sp=degreesPerSecond)
    motorLeft.run_timed(time_sp=timeOfMovement * 1000, speed_sp=degreesPerSecond)
    
    sleep(timeOfMovement + 0.5)
    #Sensor Data
    #Final reading for the tachometer of each wheel
    finalTachoReadingLeft = motorLeft.position
    finalTachoReadingRight = motorRight.position 

    #Get the delta for the tachometer of each wheel, this will give us the actual
    #number of degrees that each wheel rotated
    tachoDeltaLeft =  finalTachoReadingLeft - startingTachoReadingLeft
    tachoDeltaRight = finalTachoReadingRight - startingTachoReadingRight

    #We use a simple rule of 3 to calculate the distance travelled by each wheel
    #This distance is in meters
    distanceLeft = (tachoDeltaLeft*wheelCircumference)/360
    distanceRight = (tachoDeltaRight*wheelCircumference)/360

    #Get the average of the two distance traversed by each wheel. Getting this average
    #should give us the distance of the midpoint of the two weels a.k.a the center of the axle
    distanceTraversed = (distanceLeft + distanceRight)/2

    print("The distance entered was: " + str(distance) + " meters")
    print("The distance as calculated by using the tachometer was: " + str(distanceTraversed) + " meters")
    print("The absolute error is " + str(distance - distanceTraversed))
    print("The relative error is "+ str((distance - distanceTraversed)/distanceTraversed))


#angle:float. The angle we want the robot to rotate (in degrees, must be positive)
#degreesPerSecond:integer. (Optional Parameter) the degrees per second the wheels are supposed to rotate
#                     in this case the right wheel will turn degreesPerSecond and the left -degreesPerSecond 
#returns: float. The error, defined by the actual distance (according to the enconders)
#                and the expected distance
def rotationError(angle, degreesPerSecond=270):
    
    degreesPerSecondInRadians = (degreesPerSecond*2*pi)/360

    intialValue = gy.value()
    #In meters
    robotAxle = 11.7/100
    #The circle that the robots draws when rotating in place
    circumference = (robotAxle*pi)

    #In meters per second (radius of wheel * angular velocity of wheel (radians per second))
    velocityOfLeftWheel = -(degreesPerSecondInRadians)*(wheelDiameter/2)
    velocityOfRightWheel = (degreesPerSecondInRadians)*(wheelDiameter/2)

    #Angular velocity of vehicle in radians per second
    angularVelocityOfVehicle = (velocityOfRightWheel - velocityOfLeftWheel)/robotAxle

    #We convert the given angle of rotation to radians
    angleInRadians = (angle*2*pi)/360

    #Time that the robot should be moving at the given angular velocity in order to rotate
    #   the amound given specified by the given angle. This is in seconds
    timeOfMovement = angleInRadians/angularVelocityOfVehicle

    print("Time of movement " + str(timeOfMovement))
    motorRight.run_timed(time_sp=int(timeOfMovement * 1000), speed_sp=degreesPerSecond)
    motorLeft.run_timed(time_sp=int(timeOfMovement * 1000), speed_sp=-degreesPerSecond)
    sleep(timeOfMovement/1000 + 0.5)

    endAngle = abs(gy.value()- intialValue)

    print("The angle entered was: " + str(angle) + " degrees")
    print("The angle as calculated by using the gyroscope was: " + str(endAngle) + " degrees")
    print("The absolute error is " + str(angle - endAngle))
    print("The relative error is "+ str((angle - endAngle)/endAngle))


print("Rotation")
rotationError(90)
sleep(3)
print("Straight Line")
straightLineError(0.35)