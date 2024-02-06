import struct
import sys
import time
from queue import Queue
import json
import threading
import math
import pigpio
from nrf24 import *
from src.Libs.controller import PS4Controller
import pygame

from src.Libs.tools.paths import MOTORS_SETTINGS_PATH, TRANSMITT_SETTINGS_PATH

with open(TRANSMITT_SETTINGS_PATH) as data:
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
nrf.open_writing_pipe(address,size=getattr(RF24_PAYLOAD,tx_settings["payload_size"]["value"]))
    
    # Display the content of NRF24L01 device registers.
nrf.show_registers()

def file_to_bytearray(prefix:bytes,file_path:str):
    with open() as data:
        b = bytes(data.read(),'utf-8')
            
        for i in range(int(math.ceil(len(b)/31))):
            s = list(b[i*31:i*31+31])
            s[:0]=[prefix]
            yield s


class Tx_Thread(threading.Thread):
    def __init__(self) -> None:
        self.controller = PS4Controller()
        super().__init__()

    def callback(self):
        nrf.power_down()
        pi.stop()

    def run(self):
        sends=self.controller.get_data()
        payload=None
        send_state = 1
        try:
            while True:
                if sends:
                                    
                    if sends[9] and sends[10]:
                        for s in file_to_bytearray(0x03,MOTORS_SETTINGS_PATH):
                            nrf.send(s)
                            nrf.wait_until_sent()

                        for s in file_to_bytearray(0x04,TRANSMITT_SETTINGS_PATH):
                            nrf.send(s)
                            nrf.wait_until_sent()

                        nrf.send(0x05)
                        
                    else:     
                        if send_state == 0: #Not active
                            send_state = 1
                        elif send_state == 1:
                            payload = struct.pack("<B"+"f"*6, #Axis data
                                            0x02,
                                            *sends[:5])
                            send_state = 1
                        nrf.reset_packages_lost()
                        nrf.send(payload)                      
                try:
                    if payload:
                        nrf.wait_until_sent()

                except TimeoutError:
                    time.sleep(0.2)
                    continue
                                    
        except KeyboardInterrupt:
            nrf.power_down()
            pi.stop()
            
            

     