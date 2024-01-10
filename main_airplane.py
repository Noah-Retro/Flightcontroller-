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
from src.Libs.actors import CustomServo
from src.Libs.sensors import MPU_9250
import timeit

servo17 = CustomServo(17,clamp_min=0,clamp_max=2)

button_queue = Queue()
axis_queue = Queue()
tx = Rx_Thread(button_queue=button_queue,axis_queue=axis_queue)
tx.start()

mpu = MPU_9250()


try:
    db = DbHandler()
except sqlite3.OperationalError as e:
    print(e)
    dled.progLed(Status.DBERROR,LEDS.DATALED)
      
with open("./src/settings/data.json","r") as data:
    settings = json.load(data)
with open("./src/settings/data.json","w") as data:
    settings["fligth_num"]+=1
    data.write(json.dumps(settings,indent=4))

dled.progLed(Status.READY,LEDS.PROGLED)

def main():
    while True: 
        db.storeMPUData(mpu.dataFrame)
        try:       
            if not axis_queue.empty():
                for _ in range(axis_queue.qsize()-1):
                    data = axis_queue.get_nowait()
                servo17.setVal(data[4])
                
        except KeyboardInterrupt:
            dled.clear()
            tx.join()
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

