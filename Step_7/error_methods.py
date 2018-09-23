#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make robot move in a straight line

from time import sleep
from ev3dev.ev3 import *

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
#Degrees per second for the wheels
degreesPerSecond = 180
#Wheel circumference in meters
wheelCircumference = wheelDiameter*pi
#Speed for the wheels, in meters per second
wheelVelocity = ((wheelCircumference)*(degreesPerSecond/360))
#-------------------------

assert motorRight.connected
assert motorLeft.connected

Leds.set_color(Leds.LEFT,  Leds.ORANGE)
sleep(0.5)


#distance:float. Distance that we want the robot to travel in meters (must be positive)
#returns: float. The error, defined by the actual distance (according to the enconders)
#                and the expected distance
def straightLineError(distance):
    #In seconds
    timeOfMovement = (x/wheelVelocity)
    #Sensor Data
    #Current reading of the tachometer of each wheel  (in degrees)
    startingTachoReadingLeft = motorLeft.position
    startingTachoReadingRight = motorRight.position

    motorRight.run_timed(time_sp=timeOfMovement * 1000, speed_sp=180)
    motorLeft.run_timed(time_sp=timeOfMovement * 1000, speed_sp=180)
    
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
#returns: float. The error, defined by the actual distance (according to the enconders)
#                and the expected distance
def rotationError(angle):

    startAngle = gy.value()
    #Total distance that the robot has to "traverse", represented the longitude the arc of the
    #circle formed when the robot rotates in place by "angle" degrees 
    arcLength = (degrees/360)*wheelCircumference
    
    #In seconds
    timeOfMovement = (arcLength/wheelVelocity)

    motorRight.run_timed(time_sp=timeOfMovement * 1000, speed_sp=180)
    motorLeft.run_timed(time_sp=timeOfMovement * 1000, speed_sp=-180)
    sleep(timeOfMovement + 0.5)

    endAngle = gy.value()
    angleDelta = endAngle - startAngle

    print("The angle entered was: " + str(angle) + " degrees")
    print("The distance as calculated by using the gyroscope was: " + str(angleDelta) + " meters")
    print("The absolute error is " + str(angle - angleDelta))
    print("The relative error is "+ str((angle - angleDelta)/angleDelta))
