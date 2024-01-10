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
import numpy as np



pi = pigpio.pi()

if not pi.connected:
   exit()

class CustomServo():
    def __init__(self,pin:int,clamp_min:int=0,clamp_max:int=2) -> None:
        self.pin = pin
        self.MIN_WIDTH=950
        self.MAX_WIDTH=2100
        self.clamp_min = clamp_min
        self.clamp_max = clamp_max
    
    def scale(self,ins:float):
        res = (self.MAX_WIDTH-self.MIN_WIDTH) * np.clip((ins+1)/2,self.clamp_min,self.clamp_max) + self.MAX_WIDTH        
        return int(res)
        
    def setVal(self,ins:int):
        pi.set_servo_pulsewidth(self.pin,self.scale(ins))
        
    def stop(self):
        pi.set_servo_pulsewidth(self.pin,0)

if __name__=="__main__":
    servof = CustomServo(17)
    
    while True:
        try:
            for i in range(100):
                r = (i+ 0.01)/50 
                print(r)
                servof.setVal(r)
                time.sleep(0.1)

        except KeyboardInterrupt:
            pi.set_servo_pulsewidth(17, 0)
            pi.stop()




