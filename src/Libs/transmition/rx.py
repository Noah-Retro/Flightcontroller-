import argparse
from collections.abc import Callable, Iterable, Mapping
from datetime import datetime
import struct
import sys
import time
import traceback
import json
import threading
from typing import Any
from queue import Queue

import pigpio
from nrf24 import *

data = open("src/settings/transmitt.json")
settings = json.load(data)
rx_settings = settings["rx"]

hostname = rx_settings["hostname"]
port = rx_settings["port"]
address = rx_settings["address"]

pi = pigpio.pi(hostname, port)
if not pi.connected:
    print("Not connected to Raspberry Pi ... goodbye.")
    sys.exit()

SPI_CHANNEL.MAIN_CE0

nrf = NRF24(pi, 
            ce=rx_settings["ce"],
            payload_size=getattr(RF24_PAYLOAD,rx_settings["payload_size"]["value"]),
            channel=rx_settings["channel"],
            data_rate=getattr(RF24_DATA_RATE,rx_settings["data_rate"]["value"]),
            pa_level=getattr(RF24_PA,rx_settings["pa_level"]["value"]))
nrf.set_address_bytes(len(address))

# Listen on the address specified as parameter
nrf.open_reading_pipe(RF24_RX_ADDR.P1, address,size=getattr(RF24_PAYLOAD,rx_settings["payload_size"]["value"]))
   
# Display the content of NRF24L01 device registers.
nrf.show_registers()

class Rx_Thread(threading.Thread):
    def __init__(self,button_queue:Queue,axis_queue:Queue) -> None:
        self.button_queue=button_queue
        self.axis_queue = axis_queue
        super().__init__()

    def callback(self):
        nrf.power_down()
        pi.stop()      

    def run(self):
        count = 0

        while True:
            while nrf.data_ready():           
                count += 1
                now = datetime.now()
                
                pipe = nrf.data_pipe()              
                payload = nrf.get_payload()                                             
                
                protocol = payload[0] if len(payload) > 0 else -1            

                hex = ':'.join(f'{i:02x}' for i in payload)
                
                if payload[0] == 0x01:
                    values = struct.unpack("<B"+"?"*13, payload)
                    self.button_queue.put_nowait(values)
                if payload[0] == 0x02:
                    values = struct.unpack("<B"+"f"*6, payload)
                    self.axis_queue.put_nowait(values)

                

            

