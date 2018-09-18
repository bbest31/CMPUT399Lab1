#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make robot move in a circle

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

startAngle = gy.value()
while(gy.value() <= startAngle + 360):
    motorLeft.run_forever(speed_sp=180)
    motorRight.run_forever(speed_sp=45)
motorLeft.stop()
motorRight.stop()



