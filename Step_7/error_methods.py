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


rotation(20)



#distance:float. Distance that we want the robot to travel in meters
#returns: float. The error, defined by the actual distance (according to the enconders)
#                and the expected distance
def straightLineError(distance):
    return 0


#angle:float. The angle we want the robot to rotate (in degrees)
#returns: float. The error, defined by the actual distance (according to the enconders)
#                and the expected distance
def rotationError(angle):

    startAngle = gy.value()
    motorRight.run_timed(time_sp=10 * 1000, speed_sp=180)
    motorLeft.run_timed(time_sp=10 * 1000, speed_sp=-180)
    sleep(10)
    print('Angle deviation = '+str(abs(startAngle-gy.value())))
    return 0