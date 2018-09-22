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

assert motorRight.connected
assert motorLeft.connected

Leds.set_color(Leds.LEFT,  Leds.ORANGE)
sleep(0.5)

# Straight line movement


def straightLine(speed, sec):
    startAngle = gy.value()
    motorRight.run_timed(time_sp=sec * 1000, speed_sp=speed)
    motorLeft.run_timed(time_sp=sec * 1000, speed_sp=speed)
    sleep(sec+1)
    print("Angle Deviation = " + str(abs(startAngle-gy.value)))


straightLine(250, 4)


# Rotating Movement


def rotation(leftSpeed, rightSpeed, sec):
    startAngle = gy.value()
    motorRight.run_timed(time_sp=sec * 1000, speed_sp=rightSpeed)
    motorLeft.run_timed(time_sp=sec * 1000, speed_sp=leftSpeed)
    sleep(sec+1)
    print('Angle deviation = '+str(abs(startAngle-gy.value())))
