#!/usr/bin/env python

# servo_demo.py
# 2016-10-07
# Public Domain

# servo_demo.py          # Send servo pulses to GPIO 4.
# servo_demo.py 23 24 25 # Send servo pulses to GPIO 23, 24, 25.

import sys
import time
import random
import pigpio

NUM_GPIO=32

MIN_WIDTH=950
MAX_WIDTH=2100

step = [0]*NUM_GPIO
width = [0]*NUM_GPIO
used = [False]*NUM_GPIO

pi = pigpio.pi()

if not pi.connected:
   exit()


def scale(input:float,_min:int=MIN_WIDTH,_max:int=MAX_WIDTH):
    res = (_max-_min)*input
    return res
    

while True:

    try:

        for i in range(100):
            r = i/100
            pi.set_servo_pulsewidth(17, scale(r))
            time.sleep(0.1)

    except KeyboardInterrupt:
        for g in G:
            pi.set_servo_pulsewidth(g, 0)

        pi.stop()




