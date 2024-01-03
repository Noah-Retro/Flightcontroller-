from collections.abc import Callable, Iterable, Mapping
from datetime import datetime
import struct
import sys
import time
from queue import Queue
import json
import threading
from typing import Any
from random import normalvariate

import pigpio
from nrf24 import *



data = open("src/settings/transmitt.json")
settings = json.load(data)
tx_settings = settings["tx"]

hostname = tx_settings["hostname"]
port = tx_settings["port"]
address = tx_settings["address"]

pi = pigpio.pi(hostname, port)
if not pi.connected:
    print("Not connected to Raspberry Pi ... goodbye.")
    sys.exit()

nrf = NRF24(pi, 
            ce=tx_settings["ce"],
            payload_size=getattr(RF24_PAYLOAD,tx_settings["payload_size"]["value"]),
            channel=tx_settings["channel"],
            data_rate=getattr(RF24_DATA_RATE,tx_settings["data_rate"]["value"]),
            pa_level=getattr(RF24_PA,tx_settings["pa_level"]["value"]))
nrf.set_address_bytes(len(address))
nrf.open_writing_pipe(address)
    
    # Display the content of NRF24L01 device registers.
nrf.show_registers()



class Tx_Thread(threading.Thread):
    def __init__(self,sending_data:Queue,is_setting:bool=False) -> None:
        self.sending_data = sending_data
        self.is_setting = is_setting
        super().__init__()

    def callback(self):
        nrf.power_down()
        pi.stop()

    def run(self):
        count = 0
        send=[]
        try:
            while True:
                if not self.sending_data.empty():
                    for _ in range(self.sending_data.qsize()-1):
                        send=self.sending_data.get_nowait()
                
                    if not send:
                        continue
                    if send[0][9] and send[0][10]:
                        pass
                    else:
                        button_bytes = struct.pack("?"*13,*send[0].values())
                        axis_bytes = struct.pack("f"*6,*send[1].values())
                        hat_bytes = struct.pack("h"*2,
                                                 send[2][0][0],
                                                 send[2][0][1])
       
                    payload = struct.pack("<BBBB", 0x01, button_bytes,axis_bytes,hat_bytes)
                    print(payload.__sizeof__())
                # Send the payload to the address specified above.
                nrf.reset_packages_lost()
                nrf.send(payload)
                try:
                    nrf.wait_until_sent()
                except TimeoutError:
                    time.sleep(0.2)
                    continue
        except KeyboardInterrupt:
            nrf.power_down()
            pi.stop()
            
            

     