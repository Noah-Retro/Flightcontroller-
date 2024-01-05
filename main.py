import src.Libs.autoupdate as ap
from src.Libs.controller import PS4Controller
from src.Libs.gui import App
from src.Libs.transmition import Tx_Thread
import pygame

from sys import platform
import os
from threading import Thread
from queue import Queue
from collections import deque
import time

try:
    if platform == "linux":
        ap.update(os.path.dirname(os.path.abspath(__file__)))
except Exception as e:
    raise e

pygame.init()
pygame.joystick.init()

while pygame.joystick.get_count()<=0:
    print("Controller not connected")
    pygame.joystick.init()

controller = pygame.joystick.Joystick(0)
controller.init()

controllerQueue = Queue()
controllerQueueSend = Queue()

ps4con = PS4Controller(controller=controller,q=controllerQueue,q1=controllerQueueSend)
rx = Tx_Thread(controllerQueueSend)
app=App("src/settings")

controllerData = []

if __name__ == '__main__':
    
    ps4con.start()
    app.start()
    #rx.start()
    
    
    #---------tEST------------
    
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

    count =  0
    
    
    
    
    
    
    
    
    
    while True:
        if not controllerQueue.empty():
            
            for _ in range(controllerQueue.qsize()-1):
                controllerData = controllerQueue.get_nowait()
        
        if len(controllerData)>0:
            if controllerData[0][0]:
                controller.rumble(low_frequency=0.5,high_frequency=1,duration=0)
            else:
                controller.stop_rumble()
                
                
        #--------tEST---------
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
            
            
            if payload[0] == 0x01:
                
                for i in payload:
                    print(i)
                print("Payload rx: " + str(struct.unpack("@B"+"?"*13+"f"*6+"h"*2, payload)))
                values = struct.unpack("<B"+"?"*13+"f"*6+"h"*2, payload)
                    
            time.sleep(0.1)
                
        
        
        
                
        
                        
        