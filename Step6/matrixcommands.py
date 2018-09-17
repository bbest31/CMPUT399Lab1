#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from ev3dev.ev3 import *

# Connect gyro
gy = GyroSensor() 

# Put the gyro sensor into ANGLE mode.
gy.mode='GYRO-ANG'

motorLeft = LargeMotor(OUTPUT_B)
motorRight = LargeMotor(OUTPUT_C)

assert motorRight.connected
assert motorLeft.connected

Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

commands = [[80,60,2],[60,60,1],[-50,80,2]]

for command in commands:
    runTime = command[2]*1000
    leftSpeed = (command[0]*0.01)*900
    rightSpeed = (command[1]*0.01)*900
    motorLeft.run_timed(time_sp=runTime, speed_sp=leftSpeed)
    motorRight.run_timed(time_sp=runTime, speed_sp=rightSpeed)
    sleep(command[2]+1)


