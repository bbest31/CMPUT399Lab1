#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make robot move in a straight line

from time import sleep
from ev3dev.ev3 import *

motorRight = LargeMotor(OUTPUT_C)
motorLeft = LargeMotor(OUTPUT_B)

assert motorRight.connected
assert motorLeft.connected

Leds.set_color(Leds.LEFT,  Leds.ORANGE)
sleep(0.5)

motorRight.run_timed(time_sp=4000, speed_sp=180)
motorLeft.run_timed(time_sp=4000, speed_sp=180)

sleep(4)


