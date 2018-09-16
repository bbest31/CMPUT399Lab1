#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make robot move in a figure-8

from time import sleep
from ev3dev.ev3 import *

motorLeft = LargeMotor(OUTPUT_B)
motorRight = LargeMotor(OUTPUT_C)

def leftCircle():
    motorLeft.run_to_rel_pos(position_sp=1569, speed_sp=180, stop_action="hold")
    motorLeft.wait_while('running')

def rightCircle():
    motorRight.run_to_rel_pos(position_sp=1569, speed_sp=180, stop_action="hold")
    motorRight.wait_while('running')

assert motorRight.connected
assert motorLeft.connected


Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

# Run
leftCircle()
rightCircle()




