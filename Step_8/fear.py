#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from ev3dev.ev3 import *

motorRight = LargeMotor(OUTPUT_C)
motorLeft = LargeMotor(OUTPUT_B)

# Connect Color Sensors
rightSensor = ColorSensor(INPUT_4)
leftSensor = ColorSensor(INPUT_2)


# Put the color sensors into AMBIENT mode.
leftSensor.mode = 'COL-AMBIENT'
rightSensor.mode = 'COL-AMBIENT'

assert motorRight.connected
assert motorLeft.connected

Leds.set_color(Leds.LEFT,  Leds.ORANGE)
sleep(0.5)

# Fear Movement


def fear(thresh):

    motorLeft.run_forever(speed_sp=280)
    motorRight.run_forever(speed_sp=280)

    while(True):
        if(rightSensor.ambient_light_intensity > thresh or leftSensor.ambient_light_intensity > thresh):
            if (rightSensor.ambient_light_intensity > leftSensor.ambient_light_intensity):
                motorRight.run_forever(speed_sp=280)
                motorLeft.run_forever(speed_sp=10)
            else:
                motorRight.run_forever(speed_sp=10)
                motorLeft.run_forever(speed_sp=280)
        else:
            motorLeft.run_forever(speed_sp=280)
            motorRight.run_forever(speed_sp=280)


def agressive(thresh):

    motorLeft.run_forever(speed_sp=280)
    motorRight.run_forever(speed_sp=280)

    while(True):
        if(rightSensor.ambient_light_intensity > thresh or leftSensor.ambient_light_intensity > thresh):
            if (rightSensor.ambient_light_intensity > leftSensor.ambient_light_intensity):
                motorLeft.run_forever(speed_sp=280)
                motorRight.run_forever(speed_sp=10)
            else:
                motorLeft.run_forever(speed_sp=10)
                motorRight.run_forever(speed_sp=280)

        #    if(rightSensor.ambient_light_intensity > 50 or leftSensor.ambient_light_intensity > 50):
        #        motorLeft.stop()
        #        motorRight.stop()
        #        break
        else:
            motorLeft.run_forever(speed_sp=280)
            motorRight.run_forever(speed_sp=280)


def love(thresh):

    motorLeft.run_forever(speed_sp=280)
    motorRight.run_forever(speed_sp=280)

    while(True):
        leftIntensity = lightSensor2.ambient_light_intensity
        rightIntensity = lightSensor1.ambient_light_intensity

        motorLeft.run_forever(speed_sp=280*((100-leftIntensity)/100))
        motorRight.run_forever(speed_sp=280*((100-rightIntensity)/100))

agressive(10)