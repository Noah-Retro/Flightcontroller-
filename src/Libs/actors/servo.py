#!/usr/bin/env python

# servo_demo.py
# 2016-10-07
# Public Domain

# servo_demo.py          # Send servo pulses to GPIO 4.
# servo_demo.py 23 24 25 # Send servo pulses to GPIO 23, 24, 25.

import datetime
import sys
import time
import random
import pigpio
import numpy as np
from typing import Protocol


pi = pigpio.pi()

if not pi.connected:
   exit()

class Motor(Protocol):
    pin:int
    MIN_WIDTH:int=950
    MAX_WIDTH:int=2100
    clamp_min:float
    clamp_max:float
    zero:float
    
    
    def scale(self,ins:float):
        raise NotImplementedError    
        
    def setVal(self,ins:int):
        pi.set_servo_pulsewidth(self.pin,self.scale(ins))
        
    def stop(self):
        pi.set_servo_pulsewidth(self.pin,0)

class CustomServo(Motor):
    def __init__(self,pin:int,clamp_min:float=0,clamp_max:float=2,zero:float=1) -> None:
        self.pin = pin
        self.MIN_WIDTH=950
        self.MAX_WIDTH=2100
        self.clamp_min = clamp_min
        self.clamp_max = clamp_max
        self.zero = zero
    
    def scale(self,ins:float):
        res = (self.MAX_WIDTH-self.MIN_WIDTH) * (np.clip((ins+(self.zero)),self.clamp_min,self.clamp_max)/(self.clamp_max)) + self.MIN_WIDTH        
        return int(res)

class CustomBrushless(Motor):
    def __init__(self,pin:int,clamp_min:float=0,clamp_max:float=2) -> None:
        self.pin = pin
        self.MIN_WIDTH=700
        self.MAX_WIDTH=2000
        self.clamp_min = clamp_min
        self.clamp_max = clamp_max

    def scale(self,ins:float):
        res = (self.MAX_WIDTH-self.MIN_WIDTH) * (np.clip((ins),self.clamp_min,self.clamp_max)/(self.clamp_max)) + self.MIN_WIDTH        
        print(res)
        return int(res) 

    def arm(self): #This is the arming procedure of an ESC 
        pi.set_servo_pulsewidth(self.pin, 0)
        time.sleep(2)
        pi.set_servo_pulsewidth(self.pin, self.MAX_WIDTH)
        time.sleep(2)
        pi.set_servo_pulsewidth(self.pin, self.MIN_WIDTH)
        time.sleep(2)
     

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




