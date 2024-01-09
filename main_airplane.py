import nrf24
from src.Libs.transmition import Rx_Thread
from threading import Thread
import time
from queue import Queue
import os
import sys
from src.Libs.db_tools import DbHandler
from src.Libs.tools import DebugLEDHandler,LEDS,Status
from src.Libs.sensors import MPU_9250

button_queue = Queue()
axis_queue = Queue()
tx = Rx_Thread(button_queue=button_queue,axis_queue=axis_queue)
#print("Started thread in 1")
tx.start()
#print("Started")

dled = DebugLEDHandler()
mpu = MPU_9250()
db = DbHandler()
mpu.run()

while True: 
    db.storeMPUData(mpu.dataFrame)
    if not button_queue.empty():
        print(button_queue.get_nowait())
    if not axis_queue.empty():
        print(axis_queue.get_nowait())
    else:
        dled.progLed(Status.TRANSMITTERROR,LEDS.DATALED)
    

