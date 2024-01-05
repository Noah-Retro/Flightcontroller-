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
    def __init__(self,queue:Queue) -> None:
        self.queue=queue
        super().__init__()

    def callback(self):
        nrf.power_down()
        pi.stop()      

    def run(self):
        count = 0

        while True:
            while nrf.data_ready():
                # Count message and record time of reception.            
                count += 1
                now = datetime.now()
                 
                # Read pipe and payload for message. 
                pipe = nrf.data_pipe()              
                payload = nrf.get_payload()                                             
                print(payload)
                # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
                # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
                protocol = payload[0] if len(payload) > 0 else -1            

                hex = ':'.join(f'{i:02x}' for i in payload)

                # Show message received as hex.
                print(f"{now:%Y-%m-%d %H:%M:%S.%f}: pipe: {pipe}, len: {len(payload)}, bytes: {hex}, count: {count}, protocol: {protocol}")
                nrf.show_registers()
                
                if payload[0] == 0x01:
                    
                    for i in payload:
                        print(i)
                    print("Payload rx: " + str(struct.unpack("@B"+"?"*13+"f"*6+"h"*2, payload)))
                    values = struct.unpack("<B"+"?"*13+"f"*6+"h"*2, payload)
                    self.queue.put_nowait(values)
            time.sleep(0.1)
                

            

