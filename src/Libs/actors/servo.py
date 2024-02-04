
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
        
    def setVal(self,ins:float):
        pi.set_servo_pulsewidth(self.pin,self.scale(ins))
        
    def stop(self):
        pi.set_servo_pulsewidth(self.pin,0)

class CustomServo(Motor):
    def __init__(self,pin:int,clamp_min:float=0,clamp_max:float=2,zero:float=1) -> None:
        self.pin = pin
        self.MIN_WIDTH=1000
        self.MAX_WIDTH=2100
        self.clamp_min = np.interp(clamp_min -1,[-1,1],[self.MIN_WIDTH,self.MAX_WIDTH])
        self.clamp_max = np.interp(clamp_max -1,[-1,1],[self.MIN_WIDTH,self.MAX_WIDTH])
        self.zero = zero-1
    
    def scale(self,ins:float):
        if self.zero <= 0:
            res = np.interp(ins,[-1-self.zero,1],[self.clamp_min,self.clamp_max])
        else:
            res = np.interp(ins,[-1,1-self.zero],[self.clamp_min,self.clamp_max])        
        return int(res)

class CustomBrushless(Motor):
    def __init__(self,pin:int,clamp_min:float=0,clamp_max:float=2) -> None:
        self.pin = pin
        self.MIN_WIDTH=700
        self.MAX_WIDTH=2000
        self.clamp_min = np.interp(clamp_min -1,[-1,1],[self.MIN_WIDTH,self.MAX_WIDTH])
        self.clamp_max = np.interp(clamp_max -1,[-1,1],[self.MIN_WIDTH,self.MAX_WIDTH])

    def scale(self,ins:float):
        res = np.interp(ins,[0,1],[self.clamp_min,self.clamp_max])
        return int(res) 

    def arm(self): #This is the arming procedure of an ESC 
        pi.set_servo_pulsewidth(self.pin, 0)
        time.sleep(2)
        pi.set_servo_pulsewidth(self.pin, self.MAX_WIDTH)
        time.sleep(4)
        pi.set_servo_pulsewidth(self.pin, self.MIN_WIDTH)
        time.sleep(2)
        pi.set_servo_pulsewidth(self.pin, 0)
     

if __name__=="__main__":
    servof = CustomBrushless(26)
    pi.set_servo_pulsewidth(13, 0)
    pi.set_servo_pulsewidth(19, 0)
    
    try:
        servof.arm()

    except KeyboardInterrupt:
        pi.set_servo_pulsewidth(26, 0)
        pi.stop()




