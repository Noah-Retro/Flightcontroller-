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
    def __init__(self) -> None:
        super().__init__()

    def callback(self):
        nrf.power_down()
        pi.stop()

    def run(self,data):
        count = 0
        while True:

            # Emulate that we read temperature and humidity from a sensor, for example
            # a DHT22 sensor.  Add a little random variation so we can see that values
            # sent/received fluctuate a bit.
            temperature = normalvariate(23.0, 0.5)
            humidity = normalvariate(62.0, 0.5)
            print(f'Sensor values: temperature={temperature}, humidity={humidity}')

            # Pack temperature and humidity into a byte buffer (payload) using a protocol 
            # signature of 0x01 so that the receiver knows that the bytes we are sending 
            # are a temperature and a humidity (see "simple-receiver.py").
            payload = struct.pack("<Bff", 0x01, temperature, humidity)

            # Send the payload to the address specified above.
            nrf.reset_packages_lost()
            nrf.send(payload)
            try:
                nrf.wait_until_sent()
            except TimeoutError:
                print('Timeout waiting for transmission to complete.')
                # Wait 10 seconds before sending the next reading.
                time.sleep(10)
                continue
            
            if nrf.get_packages_lost() == 0:
                print(f"Success: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")
            else:
                print(f"Error: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")
            time.sleep(1)

if __name__ == "__main__":
    data = 0
    sender = Tx_Thread()
    sender.run(data)       
    while not KeyboardInterrupt:
        pass        