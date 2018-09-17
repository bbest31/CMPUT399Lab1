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

def rightCircle():
    startAngle = gy.value()
    while(gy.value() != startAngle + 315):
        motorLeft.run_forever(speed_sp=180)
        motorRight.run_forever(speed_sp=45)
    motorLeft.stop()
    motorRight.stop()

def goStraight():
    motorLeft.run_to_rel_pos(position_sp=167, speed_sp=180, stop_action="hold")
    motorRight.run_to_rel_pos(position_sp=167, speed_sp=180, stop_action="hold")
    sleep(5)

def leftCircle():
    # Connect gyro
    gy = GyroSensor() 

    # Put the gyro sensor into ANGLE mode.
    gy.mode='GYRO-ANG'
    startAngle = gy.value()
    while(abs(gy.value() - startAngle) <= 315):
        motorRight.run_forever(speed_sp=180)
        motorLeft.run_forever(speed_sp=45)
        print('Gyroscope value:'+str(gy.value()) +' - Started Value: '+str(startAngle)+ ' Delta: '+str(abs(gy.value()-startAngle)))
    motorRight.stop()
    motorLeft.stop()

assert motorRight.connected
assert motorLeft.connected


Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

# Run
rightCircle()
goStraight()
leftCircle()
goStraight()



