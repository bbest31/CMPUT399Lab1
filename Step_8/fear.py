#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from ev3dev.ev3 import *

motorRight = LargeMotor(OUTPUT_C)
motorLeft = LargeMotor(OUTPUT_B)

# Connect Color Sensors
rightSensor = ColorSensor(INPUT_4)
leftSensor = ColorSensor(INPUT_2)

ultrasonicSensor = UltrasonicSensor()


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

#TODO we should check if we should change this to recompute the best intensity
def love(thresh):
    motorLeft.run_forever(speed_sp=280)
    motorRight.run_forever(speed_sp=280)
    speedModifier = 1
    previousSensorDelta = 0
    sensorDelta = 0
    while(True):
        if(rightSensor.ambient_light_intensity > thresh or leftSensor.ambient_light_intensity > thresh):
            #if this value is 0, the reading is the same for both sensors
            #   if it is less than 0 then the light is more intense for the left sensor
            #   if it is greater than 0 then the light is more intense for the right sensor
            sensorDelta = rightSensor.ambient_light_intensity - leftSensor.ambient_light_intensity
            
            #Smoother turns when delta is small
            if (abs(sensorDelta) <= 2):
                speedModifier = 15
            else:
                speedModifier = 1

            #Light is more intense for the rightSensor
            if (sensorDelta > 1):
                motorLeft.run_forever(speed_sp=280)
                motorRight.run_forever(speed_sp=10*speedModifier)
            #Light is more intense for the leftSensor
            elif (sensorDelta < -1):
                motorLeft.run_forever(speed_sp=10*speedModifier)
                motorRight.run_forever(speed_sp=280)
            else:
                motorLeft.run_forever(speed_sp=280)
                motorRight.run_forever(speed_sp=280)

            if ((rightSensor.ambient_light_intensity >= thresh*3  or leftSensor.ambient_light_intensity >= thresh*3) and abs(sensorDelta) <= 2):
                break
            previousSensorDelta = sensorDelta
        
        motorLeft.run_forever(speed_sp=280)
        motorRight.run_forever(speed_sp=280)

#Seems to work, most of the time
def explorer(thresh):
    motorLeft.run_forever(speed_sp=280)
    motorRight.run_forever(speed_sp=280)
    speedModifier = 1
    previousSensorDelta = 0
    sensorDelta = 0
    bestIntensity = 0
    while(True):
        if(rightSensor.ambient_light_intensity > thresh or leftSensor.ambient_light_intensity > thresh):
            bestIntensity = max(bestIntensity, min(rightSensor.ambient_light_intensity,leftSensor.ambient_light_intensity))
            #if this value is 0, the reading is the same for both sensors
            #   if it is less than 0 then the light is more intense for the left sensor
            #   if it is greater than 0 then the light is more intense for the right sensor
            sensorDelta = rightSensor.ambient_light_intensity - leftSensor.ambient_light_intensity
            
            #Smoother turns when delta is small
            if (abs(sensorDelta) <= 2):
                speedModifier = 15
            else:
                speedModifier = 1

            #Light is more intense for the rightSensor
            if (sensorDelta > 1):
                motorLeft.run_forever(speed_sp=280)
                motorRight.run_forever(speed_sp=10*speedModifier)
            #Light is more intense for the leftSensor
            elif (sensorDelta < -1):
                motorLeft.run_forever(speed_sp=10*speedModifier)
                motorRight.run_forever(speed_sp=280)
            else:
                motorLeft.run_forever(speed_sp=280)
                motorRight.run_forever(speed_sp=280)
            if ((rightSensor.ambient_light_intensity >= bestIntensity  or leftSensor.ambient_light_intensity >= bestIntensity) and abs(sensorDelta) <= 3):
                print(bestIntensity)
                while min(rightSensor.ambient_light_intensity,leftSensor.ambient_light_intensity) <= (bestIntensity+1):
                    motorLeft.stop()
                    motorRight.stop()    
                bestIntensity = min(rightSensor.ambient_light_intensity,leftSensor.ambient_light_intensity)              
            previousSensorDelta = sensorDelta
        
        motorLeft.run_forever(speed_sp=280)
        motorRight.run_forever(speed_sp=280)

#8 or 10 is a good threshold since the ambient light in the lab is between 4-5
#agressive(8)
#fear(8)
#love(8)
explorer(8)




def printSensorReadings():
    while(True):
        print("Left: " + str(leftSensor.ambient_light_intensity) + "    Right: " + str(rightSensor.ambient_light_intensity))
