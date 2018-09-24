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
    timeOfMovement = (distance/wheelVelocity)
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
    intialValue = gy.value()
    #In meters
    robotAxle = 10.7/100
    #The circle that the robots draws when rotating in place
    circumference = (robotAxle*pi)
    #Total distance that the robot has to "traverse", represented the longitude the arc of the
    #circle formed when the robot rotates in place by "angle" degrees 

    #We use pi because wheels are rotating 270 degrees per second
    #In meters per second
    velocityOfLeftWheel = -(3*pi/2)*(wheelDiameter/2)
    velocityOfRightWheel = (3*pi/2)*(wheelDiameter/2)

    #Angular velocity of vehicle in radians per second
    angularVelocityOfVehicle = (velocityOfRightWheel - velocityOfLeftWheel)/robotAxle

    #We convert the angle to radians
    angleInRadians = (angle*2*pi)/360

    #We use a rule of 3 to figure out how long should It take to get to the given angle
    #with the angularVelocityOfVehicle
    # this in seconds
    timeOfMovement = angleInRadians/angularVelocityOfVehicle

    print("TIme of movement " + str(timeOfMovement))
    motorRight.run_timed(time_sp=int(timeOfMovement * 1000), speed_sp=270)
    motorLeft.run_timed(time_sp=int(timeOfMovement * 1000), speed_sp=-270)
    sleep(timeOfMovement/1000 + 0.5)

    endAngle = abs(gy.value()- intialValue)

    print("The angle entered was: " + str(angle) + " degrees")
    print("The distance as calculated by using the gyroscope was: " + str(endAngle) + " degrees")
    print("The absolute error is " + str(angle - endAngle))
    print("The relative error is "+ str((angle - endAngle)/endAngle))



rotationError(90)
sleep(3)
straightLineError(0.35)