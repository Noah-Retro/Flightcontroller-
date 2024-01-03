import nrf24
from src.Libs.transmition import Rx_Thread
from threading import Thread
import time
from queue import Queue

data = Queue()
tx = Rx_Thread(data)
print("Started thread in 1")
tx.start()
print("Started")

while True:
    if data.qsize()>0:
        print(data.get_nowait())

