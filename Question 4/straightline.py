#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make robot move in a straight line

from time import sleep
from ev3dev.ev3 import *

motorRight = LargeMotor(OUTPUT_C)
motorLeft = LargeMotor(OUTPUT_B)

assert motorRight.connected
assert motorLeft.connected

Leds.all_off()

motorRight.run_timed(speed_sp=700,time_sp=700)
motorLeft.run_timed(speed_sp=700,time_sp=700)

