#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make robot move in a figure-8

from time import sleep
from ev3dev.ev3 import *

motorLeft = LargeMotor(OUTPUT_B)
motorRight = LargeMotor(OUTPUT_C)

# Connect gyro
gy = GyroSensor() 

# Put the gyro sensor into ANGLE mode.
gy.mode='GYRO-ANG'

def firstCircle():
    startAngle = gy.value()
    while(gy.value() != startAngle + 360):
        motorLeft.run_forever(speed_sp=180)
    motorLeft.stop()

def secondCircle():
    startAngle = gy.value()
    while(gy.value() != startAngle + 360):
        motorRight.run_forever(speed_sp=180)
    motorRight.stop()

assert motorRight.connected
assert motorLeft.connected


Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

# Run
firstCircle()
secondCircle()




