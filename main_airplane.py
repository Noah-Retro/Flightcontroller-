from src.Libs.tools import DebugLEDHandler,LEDS,Status
dled = DebugLEDHandler()
dled.progLed(Status.BOOTUP,LEDS.PROGLED)

import nrf24
from src.Libs.transmition import Rx_Thread
from threading import Thread
import time
from queue import Queue
import os
import sys
import sqlite3
import json
from src.Libs.db_tools import DbHandler
from src.Libs.actors import CustomServo,CustomBrushless


servo17 = CustomServo(17,clamp_min=0,clamp_max=2)
throtleR = CustomBrushless(26,clamp_min=0,clamp_max=1.5)
throtleR.arm()
servos = [servo17,throtleR]

button_queue = Queue()
axis_queue = Queue()
tx = Rx_Thread(button_queue=button_queue,axis_queue=axis_queue)
tx.start()

with open("./src/settings/data.json","r") as data:
    settings = json.load(data)
with open("./src/settings/data.json","w") as data:
    settings["fligth_num"]+=1
    data.write(json.dumps(settings,indent=4))

mpuqueue = Queue()


try:
    db = DbHandler(q=mpuqueue)
except sqlite3.OperationalError as e:
    print(e)
    dled.progLed(Status.DBERROR,LEDS.DATALED)
    
db.start()    
      
data=[None for i in range(6)]

dled.progLed(Status.READY,LEDS.PROGLED)

def main():
    while True: 
        #db.storeMPUData(mpu.dataFrame)
        try:       
            if not axis_queue.empty():
                for _ in range(axis_queue.qsize()-1):
                    data = axis_queue.get_nowait()
                    servo17.setVal(data[4])
                    throtleR.setVal(data[2]*-1)
                if data == None:
                    dled.progLed(Status.FILE_TRANSMITT,LEDS.DATALED)
                
        except KeyboardInterrupt:
            dled.clear()
            tx.join()
            db.join()
            for i in servos:
                i.stop()
            sys.exit()
            
        
        except Exception as e:
            print(e)
            dled.clear()
            dled.progLed(Status.UNKNOWNERROR,LEDS.PROGLED)
            
        else:
            dled.progLed(Status.NOSTATE,LEDS.HEALTHLED)
            dled.progLed(Status.READY,LEDS.PROGLED)
            
        finally:
            dled.clear()
            

        
main()        

