#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Make robot move in a straight line

from time import sleep
from ev3dev.ev3 import *

# Connect gyro
gy = GyroSensor() 

# Put the gyro sensor into ANGLE mode.
gy.mode='GYRO-ANG'

units = gy.units
#reports 'deg' meaning degrees

def turnLeft():
    startAngle = gy.value()
    while(gy.value() != startAngle+90):
        motorLeft.run_forever(speed_sp=180)
    motorLeft.stop()
    sleep(1)
    angle = gy.value()
    print('Angle in relation to original = '+str(angle))

def runHeight():
    startAngle = gy.value()
    motorRight.run_timed(time_sp=2000, speed_sp=180)
    motorLeft.run_timed(time_sp=2000, speed_sp=180)
    deviation = gy.value()-startAngle
    print("Angle deviation from line = "+str(deviation))
    sleep(3)

def runWidth():
    #Width
    startAngle = gy.value()
    motorRight.run_timed(time_sp=4000, speed_sp=180)
    motorLeft.run_timed(time_sp=4000, speed_sp=180)
    deviation = gy.value()-startAngle
    print("Angle deviation from line = "+str(deviation))
    sleep(5)

motorRight = LargeMotor(OUTPUT_C)
motorLeft = LargeMotor(OUTPUT_B)

assert motorRight.connected
assert motorLeft.connected

Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

#Rectangle
runHeight()
turnLeft()
runWidth()
turnLeft()
runHeight()
turnLeft()
runWidth()
turnLeft()






