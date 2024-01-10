import nrf24
from src.Libs.transmition import Rx_Thread
from threading import Thread
import time
from queue import Queue
import os
import sys
import sqlite3
from src.Libs.db_tools import DbHandler
from src.Libs.tools import DebugLEDHandler,LEDS,Status
from src.Libs.sensors import MPU_9250


dled = DebugLEDHandler()
dled.progLed(Status.BOOTUP,LEDS.PROGLED)
dled.show()
button_queue = Queue()
axis_queue = Queue()
tx = Rx_Thread(button_queue=button_queue,axis_queue=axis_queue)
tx.start()

mpu = MPU_9250()
mpu.run()
dled.progLed(Status.BOOTUP,LEDS.PROGLED)
dled.show()
try:
    db = DbHandler()
except sqlite3.OperationalError as e:
    print(e)
    dled.progLed(Status.DBERROR,LEDS.DATALED)
    dled.show()
    
dled.progLed(Status.READY,LEDS.PROGLED)
dled.show()

while True: 
    db.storeMPUData(mpu.dataFrame)
    try:
        #try:
        
        #except sqlite3.OperationalError as e:
        #    print(e)
        #    dled.progLed(Status.DBERROR,LEDS.DATALED)
        #else:
        #    dled.progLed(Status.NOSTATE,LEDS.DATALED)
        
        if not axis_queue.empty():
            for _ in range(axis_queue.qsize()-1):
                print(axis_queue.get_nowait())
            
    except KeyboardInterrupt:
        dled.clear()
        tx.join()
        sys.exit()
    
    except Exception as e:
        dled.progLed(Status.UNKNOWNERROR,LEDS.PROGLED)
    
    else:
        dled.progLed(Status.NOSTATE,LEDS.HEALTHLED)
        dled.progLed(Status.READY,LEDS.PROGLED)
        dled.show()
    

