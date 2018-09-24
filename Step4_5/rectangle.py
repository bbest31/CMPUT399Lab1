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

def turnRight():
    gy = GyroSensor() 
    gy.mode='GYRO-ANG'
    
    firstReading = gy.angle
    sleep(0.5)
    currentGyroAngle = 0
    print('start angle = '+str(firstReading))
    while(currentGyroAngle <= 90):
        motorLeft.run_forever(speed_sp=45)
        motorRight.run_forever(speed_sp=-45)
        currentGyroAngle = abs(gy.angle-firstReading)
        print(str(currentGyroAngle))
    motorLeft.stop()
    motorRight.stop()
    sleep(1)
    angle = gy.value()
    print('final angle = '+str(angle))

    print('Angle in relation to original = '+str(angle-firstReadings))

def runHeight():
    startAngle = gy.value()
    motorRight.run_timed(time_sp=1000, speed_sp=180)
    motorLeft.run_timed(time_sp=1000, speed_sp=180)
    deviation = gy.value()-startAngle
    print("Angle deviation from line = "+str(deviation))
    sleep(2)

def runWidth():
    #Width
    startAngle = gy.value()
    motorRight.run_timed(time_sp=2000, speed_sp=180)
    motorLeft.run_timed(time_sp=2000, speed_sp=180)
    deviation = gy.value()-startAngle
    print("Angle deviation from line = "+str(deviation))
    sleep(3)

motorRight = LargeMotor(OUTPUT_C)
motorLeft = LargeMotor(OUTPUT_B)

assert motorRight.connected
assert motorLeft.connected

Leds.set_color(Leds.LEFT,  Leds.RED)
sleep(0.5)

numberOfRectangles=3


for i in range(0,numberOfRectangles):
    #Rectangle
    runHeight()
    turnRight()
    runWidth()
    turnRight()
    runHeight()
    turnRight()
    runWidth()
    turnRight()
    sleep(0.5)






