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

        else:
            motorLeft.run_forever(speed_sp=280)
            motorRight.run_forever(speed_sp=280)

# TODO we should check if we should change this to recompute the best intensity


def love(thresh):
    motorLeft.run_forever(speed_sp=280)
    motorRight.run_forever(speed_sp=280)
    speedModifier = 1
    previousSensorDelta = 0
    sensorDelta = 0
    while(True):
        if(rightSensor.ambient_light_intensity > thresh or leftSensor.ambient_light_intensity > thresh):
            # if this value is 0, the reading is the same for both sensors
            #   if it is less than 0 then the light is more intense for the left sensor
            #   if it is greater than 0 then the light is more intense for the right sensor
            sensorDelta = rightSensor.ambient_light_intensity - \
                leftSensor.ambient_light_intensity

            # Smoother turns when delta is small
            if (abs(sensorDelta) <= 2):
                speedModifier = 15
            else:
                speedModifier = 1

            # Light is more intense for the rightSensor
            if (sensorDelta > 1):
                motorLeft.run_forever(speed_sp=280)
                motorRight.run_forever(speed_sp=10*speedModifier)
            # Light is more intense for the leftSensor
            elif (sensorDelta < -1):
                motorLeft.run_forever(speed_sp=10*speedModifier)
                motorRight.run_forever(speed_sp=280)
            else:
                motorLeft.run_forever(speed_sp=280)
                motorRight.run_forever(speed_sp=280)

            if ((rightSensor.ambient_light_intensity >= thresh*5 or leftSensor.ambient_light_intensity >= thresh*5) and abs(sensorDelta) <= 2):
                break
            # if(ultrasonicSensor.distance_centimeters < 4):
            #   break
            previousSensorDelta = sensorDelta

        motorLeft.run_forever(speed_sp=280)
        motorRight.run_forever(speed_sp=280)


def adjust(i):
    if(i == 0):
        motorRight.run_forever(speed_sp=200)
        motorLeft.run_forever(speed_sp=280)

    else:
        motorRight.run_forever(speed_sp=280)
        motorLeft.run_forever(speed_sp=200)


def explorer(thresh):
    motorLeft.run_forever(speed_sp=280)
    motorRight.run_forever(speed_sp=280)
    i = 0
    bestIntensity = thresh
    while(True):
        if(rightSensor.ambient_light_intensity > thresh or leftSensor.ambient_light_intensity > thresh):
            bestIntensity = max(bestIntensity, max(
                rightSensor.ambient_light_intensity, leftSensor.ambient_light_intensity))
            if(rightSensor.ambient_light_intensity > leftSensor.ambient_light_intensity):
                i = 0
            else:
                i = 1
            if(max(rightSensor.ambient_light_intensity, leftSensor.ambient_light_intensity) < bestIntensity-12):
                while(max(rightSensor.ambient_light_intensity, leftSensor.ambient_light_intensity) <= bestIntensity-5):
                    adjust(i)
        motorLeft.run_forever(speed_sp=280)
        motorRight.run_forever(speed_sp=280)


# 8 or 10 is a good threshold since the ambient light in the lab is between 4-5
# agressive(8)
# fear(8)
# love(8)
#explorer(3)
