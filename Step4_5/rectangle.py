#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make robot move in a straight line

from time import sleep
from ev3dev.ev3 import *
from math import *

# Connect gyro
gy = GyroSensor()

# Put the gyro sensor into ANGLE mode.
gy.mode = 'GYRO-ANG'

units = gy.units
# reports 'deg' meaning degrees

def turnRight():
    gy = GyroSensor()
    gy.mode = 'GYRO-ANG'

    firstReading = gy.angle
    sleep(0.5)
    currentGyroAngle = gy.value()
    print(str(currentGyroAngle))
    while(abs(currentGyroAngle - gy.value()) < 90):
        print(str(gy.value()))
        motorLeft.run_forever(speed_sp=120)
        motorRight.run_forever(speed_sp=-120)
    motorLeft.stop()
    motorRight.stop()
    sleep(1)


def runHeight():
    motorRight.run_timed(time_sp=3000, speed_sp=180)
    motorLeft.run_timed(time_sp=3000, speed_sp=180)
    sleep(2)


def runWidth():
    # Width
    motorRight.run_timed(time_sp=4000, speed_sp=180)
    motorLeft.run_timed(time_sp=4000, speed_sp=180)
    sleep(3)


motorRight = LargeMotor(OUTPUT_C)
motorLeft = LargeMotor(OUTPUT_B)

assert motorRight.connected
assert motorLeft.connected

Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

numberOfRectangles = 3


for i in range(0, numberOfRectangles):
    # Rectangle
    runHeight()
    turnRight()
    runWidth()
    turnRight()
    runHeight()
    turnRight()
    runWidth()
    sleep(0.5)
