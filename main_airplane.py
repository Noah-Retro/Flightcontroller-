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

print(os.path.abspath('.'))



dled = DebugLEDHandler()
dled.progLed(Status.BOOTUP,LEDS.HEALTHLED)
dled.show()
button_queue = Queue()
axis_queue = Queue()
tx = Rx_Thread(button_queue=button_queue,axis_queue=axis_queue)
tx.start()

mpu = MPU_9250()
mpu.run()
dled.progLed(Status.READY,LEDS.HEALTHLED)
dled.show()
try:
    db = DbHandler()
except sqlite3.OperationalError as e:
    dled.progLed(Status.DBERROR,LEDS.DATALED)
    dled.show()
    

while True: 
    try:
        try:
            db.storeMPUData(mpu.dataFrame)
        except Exception as e:
            dled.progLed(Status.DBERROR,LEDS.DATALED)
        if not axis_queue.empty():
            print(axis_queue.get_nowait())
        else:
            dled.progLed(Status.TRANSMITTERROR,LEDS.DATALED)
    except KeyboardInterrupt:
        dled.clear()
        sys.exit()
    except Exception as e:
        dled.progLed(Status.UNKNOWNERROR,LEDS.HEALTHLED)
    else:
        dled.show()
    

