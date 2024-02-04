import struct
import sys
import time
from queue import Queue
import json
import threading
import math
import pigpio
from nrf24 import *


with open("src/settings/transmitt.json") as data:
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
        sends=[]
        payload=None
        send_state = 1
        try:
            while True:
                if not self.sending_data.empty():
                    for _ in range(self.sending_data.qsize()-1):
                        sends=self.sending_data.get_nowait()
                
                    if not sends:
                        continue
                    if sends[0][9] and sends[0][10]:
                        with open("src/settings/motors.json") as data:
                            b = bytes(data.read(),'utf-8')
                            
                        for i in range(int(math.ceil(len(b)/31))):
                            s = list(b[i*31:i*31+31])
                            s[:0]=[0x03]
                            nrf.send(s)
                            nrf.wait_until_sent()

                        with open("src/settings/transmitt.json") as data:
                            b = bytes(data.read(),'utf-8')

                        for i in range(int(math.ceil(len(b)/31))):
                            s = list(b[i*31:i*31+31])
                            s[:0]=[0x04]
                            nrf.send(s)
                            nrf.wait_until_sent()
                        nrf.send(0x05)
                        
                    else:     
                        if send_state == 0: #Not active
                            payload = struct.pack("<B"+"?"*13, #Button data
                                            0x01,
                                            *sends[0].values())
                            send_state += 1
                        elif send_state == 1:
                            payload = struct.pack("<B"+"f"*6, #Axis data
                                            0x02,
                                            *sends[1].values())
                            send_state = 1
                        nrf.reset_packages_lost()
                        nrf.send(payload)    
                    print(payload)                   
                try:
                    if payload:
                        nrf.wait_until_sent()

                except TimeoutError:
                    time.sleep(0.2)
                    continue
                                    
        except KeyboardInterrupt:
            nrf.power_down()
            pi.stop()
            
            

     