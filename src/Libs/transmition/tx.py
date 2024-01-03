from collections.abc import Callable, Iterable, Mapping
from datetime import datetime
import struct
import sys
import time
import traceback
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
    def __init__(self,sending_data,is_setting:bool=False) -> None:
        super().__init__(daemon=True,args=(sending_data,is_setting))

    def callback(self):
        nrf.power_down()
        pi.stop()

    def run(self,sending_data,is_setting):
        count = 0
        while True:

            print(sending_data)
            payload = struct.pack("<Bf", 0x01, 0.1)

            # Send the payload to the address specified above.
            nrf.reset_packages_lost()
            nrf.send(payload)
            try:
                nrf.wait_until_sent()
            except TimeoutError:
                time.sleep(0.2)
                continue
            
            

     