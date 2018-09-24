#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make robot move in a straight line

from time import sleep
from ev3dev.ev3 import *
from math import *

# Connect gyro
gy = GyroSensor() 

# Put the gyro sensor into ANGLE mode.
gy.mode='GYRO-ANG'

units = gy.units
#reports 'deg' meaning degrees

def rotation(angle):
    wheelDiameter = 5.5/100

    #In meters
    robotAxle = 10.7/100
    #The circle that the robots draws when rotating in place
    circumference = (robotAxle*pi)
    #Total distance that the robot has to "traverse", represented the longitude the arc of the
    #circle formed when the robot rotates in place by "angle" degrees 

    #We use pi because wheels are rotating 90 degrees per second
    #In meters per second
    velocityOfLeftWheel = (3*pi/2)*(wheelDiameter/2)
    velocityOfRightWheel = -(3*pi/2)*(wheelDiameter/2)

    #Angular velocity of vehicle in radians per second
    angularVelocityOfVehicle = (velocityOfRightWheel - velocityOfLeftWheel)/robotAxle

    #We convert the angle to radians
    angleInRadians = (angle*2*pi)/360

    #We use a rule of 3 to figure out how long should It take to get to the given angle
    #with the angularVelocityOfVehicle
    # this in seconds
    timeOfMovement = angleInRadians/angularVelocityOfVehicle

    motorRight.run_timed(time_sp=int(timeOfMovement * 1000), speed_sp=-270)
    motorLeft.run_timed(time_sp=int(timeOfMovement * 1000), speed_sp=270)
    sleep(timeOfMovement/1000 + 1)




def turnRight():
    gy = GyroSensor() 
    gy.mode='GYRO-ANG'

    firstReading = gy.angle
    sleep(0.5)
    currentGyroAngle = gy.value()
    print(str(currentGyroAngle))
    while(abs(currentGyroAngle - gy.value()) < 90):
        print(str(gy.value()))
        motorLeft.run_forever(speed_sp=-45)
        motorRight.run_forever(speed_sp=45)
    motorLeft.stop()
    motorRight.stop()
    sleep(1)

def runHeight():
    motorRight.run_timed(time_sp=2000, speed_sp=180)
    motorLeft.run_timed(time_sp=2000, speed_sp=180)
    sleep(2)

def runWidth():
    #Width
    motorRight.run_timed(time_sp=3000, speed_sp=180)
    motorLeft.run_timed(time_sp=3000, speed_sp=180)
    sleep(3)

motorRight = LargeMotor(OUTPUT_C)
motorLeft = LargeMotor(OUTPUT_B)

assert motorRight.connected
assert motorLeft.connected

Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

numberOfRectangles=1


for i in range(0,numberOfRectangles):
    #Rectangle
    runHeight()
    rotation(90)
    runWidth()
    rotation(90)
    runHeight()
    rotation(90)
    runWidth()
    rotation(90)
    sleep(0.5)






