import json
import neopixel
import board
import time

class Status():
    NOSTATE=[0,0,0]
    BOOTUP=[255,0,0]
    WAITING=[255,255,0]
    READY=[0,255,0]
    UNKNOWNERROR=[255,255,255]
    VOLTAGELOW=[255,0,0]
    I2CERROR=[0,255,0]
    SPIERROR=[0,0,255]
    TRANSMITTERROR=[255,0,0]
    DBERROR=[0,0,255]
    SETTINGSERROR=[0,255,0]
       
class LEDS():   
    DATALED=0
    HEALTHLED=1
    PROGLED=2

class DebugLEDHandler():
    def __init__(self):
        self.pixel = neopixel.NeoPixel(board.D18,3)
        
    def progLed(self,state:Status,place:int,pin:int=19):
        self.pixel[place]=tuple(state)
        self.pixel.show()

if __name__ == "__main__":
    DLed = DebugLEDHandler()
    for key, value in Status.__dict__.items():
        DLed.progLed(value,LEDS.DATALED)
        DLed.progLed(value,LEDS.PROGLED)
        DLed.progLed(value,LEDS.HEALTHLED)
        time.sleep(1)