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



pi = pigpio.pi()

if not pi.connected:
   exit()

class CustomServo():
    def __init__(self,pin:int) -> None:
        self.pin = pin
        self.MIN_WIDTH=950
        self.MAX_WIDTH=2100
    
    def scale(self,ins:float,_min:int=950,_max:int=2100):
        res = (_max-_min) * (ins+1)/2 + _min
        return int(res)
        
    def setVal(self,ins:int):
        print(self.pin,": ",self.scale(ins))
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




