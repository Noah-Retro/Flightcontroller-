import nrf24
from src.Libs.transmition import Rx_Thread
from threading import Thread
import time

data = None
tx = Rx_Thread(data)
print("Started thread in 1")
tx.start()
print("Started")

while True:
    print(data)
    time.sleep(10)
