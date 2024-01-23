import neopixel
import board
import time

class Status():
    NOSTATE=[0,0,0] #Allgemein
    UNKNOWNERROR=[255,255,255]
    
    BOOTUP=[255,0,0] #Prog Led
    READY=[0,255,0]
    
    VOLTAGELOW=[255,0,0] #Health statuss
    
    DBERROR=[0,0,255] #Data Led status
    SETTINGSERROR=[0,255,0]
    FILE_TRANSMITT=[255,0,0]#[Rot,Grün,Blau]
       
class LEDS():   
    DATALED=0
    HEALTHLED=1
    PROGLED=2

class DebugLEDHandler():   
    def __init__(self):
        self.pixel = neopixel.NeoPixel(board.D18,3)
        
    def progLed(self,state:Status,place:int,pin:int=19):
        self.pixel[place]=tuple(state)
        
    def clear(self):
        self.pixel.fill((0,0,0))
        self.pixel.show()
        
    def clearLED(self,led:int):
        self.pixel[led]=(0,0,0)
        
    def show(self):
        self.pixel.show()

if __name__ == "__main__":
    DLed = DebugLEDHandler()
    DLed.progLed(Status.UNKNOWNERROR,LEDS.DATALED)
    DLed.progLed(Status.UNKNOWNERROR,LEDS.PROGLED)
    DLed.progLed(Status.UNKNOWNERROR,LEDS.HEALTHLED)
    time.sleep(1)
    DLed.clear()
    