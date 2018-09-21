#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from ev3dev.ev3 import *
from math import *
# Connect gyro
gy = GyroSensor() 

# Put the gyro sensor into ANGLE mode.
gy.mode='GYRO-ANG'

motorLeft = LargeMotor(OUTPUT_B)
motorRight = LargeMotor(OUTPUT_C)

assert motorRight.connected
assert motorLeft.connected

pos = [0,0]
wheelCircumference = 17.3
axelDiameter = 14.5

Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

# commands correspond to [left-motor-speed, right-motor-speed, time duration (s)]
# commands = [[80,60,2],[60,60,1],[-50,80,2]]
 commands = [[80,60,2]]
# Run the commands given in the variable
for command in commands:
    runTime = command[2]*1000
    leftSpeed = (command[0]*0.01)*900
    rightSpeed = (command[1]*0.01)*900
    currentAngle = gy.value()
    motorLeft.run_timed(time_sp=runTime, speed_sp=leftSpeed)
    motorRight.run_timed(time_sp=runTime, speed_sp=rightSpeed)
    updateCoordinates(leftSpeed,rightSpeed,command[2])
    sleep(command[2]+1)

def updateCoordinates(leftSpeed, rightSpeed, sec):
    #Calculate Vl and Vr
    leftVelocity = leftSpeed*wheelCircumference/360*sec
    rightVelocity = rightSpeed*wheelCircumference/360*sec

    velocity = (leftVelocity + rightVelocity)/2

    omega = (rightVelocity - leftVelocity)/axelDiameter
    
    theta = (wheelCircumference*rightSpeed - wheelCircumference*leftSpeed)*log(sec)/5220

