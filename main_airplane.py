import copy
from src.Libs.tools.debug_leds import DebugLEDHandler,LEDS,Status
dled = DebugLEDHandler()
dled.progLed(Status.BOOTUP,LEDS.PROGLED)

import nrf24
from src.Libs.transmition import Rx_Thread
from threading import Thread
import time
from multiprocessing import Queue
import os
import sys
import sqlite3
import json
from src.Libs.db_tools import DbHandler
from src.Libs.actors import CustomServo,CustomBrushless
from src.Libs.tools.paths import MOTORS_SETTINGS_PATH,CONTROLLER_SETTINGS_PATH,DATA_SETTINGS_PATH

with open(MOTORS_SETTINGS_PATH) as motors_file:
            motor_data = json.load(motors_file)

servoRL = CustomServo(motor_data["leftRight"]["pin"],
                      clamp_min=motor_data["leftRight"]["clamp_min"],
                      clamp_max=motor_data["leftRight"]["clamp_max"],
                      zero=motor_data["leftRight"]["zero"])
servoUDR = CustomServo(motor_data["rightUD"]["pin"],
                      clamp_min=motor_data["rightUD"]["clamp_min"],
                      clamp_max=motor_data["rightUD"]["clamp_max"],
                      zero=motor_data["rightUD"]["zero"])
servoUDL = CustomServo(motor_data["leftUD"]["pin"],
                      clamp_min=motor_data["leftUD"]["clamp_min"],
                      clamp_max=motor_data["leftUD"]["clamp_max"],
                      zero=motor_data["leftUD"]["zero"])
throtleR = CustomBrushless(motor_data["throtleR"]["pin"],
                      clamp_min=motor_data["throtleR"]["clamp_min"],
                      clamp_max=motor_data["throtleR"]["clamp_max"])
throtleL = CustomBrushless(motor_data["throtleL"]["pin"],
                      clamp_min=motor_data["throtleL"]["clamp_min"],
                      clamp_max=motor_data["throtleL"]["clamp_max"])
servos = [
    servoRL, 
    servoUDR,
    servoUDL,
    throtleR,
    throtleL
]

button_queue = Queue()
axis_queue = Queue()
tx = Rx_Thread(button_queue=button_queue,axis_queue=axis_queue)
tx.start()

with open(DATA_SETTINGS_PATH,"r") as data:
    settings = json.load(data)
with open(DATA_SETTINGS_PATH,"w") as data:
    settings["fligth_num"]+=1
    data.write(json.dumps(settings,indent=4))

mpuqueue = Queue()


try:
    db = DbHandler(q=mpuqueue)
except Exception as e:
    print(e)
    dled.progLed(Status.DBERROR,LEDS.DATALED)
    
#db.start()    
      
dled.progLed(Status.READY,LEDS.PROGLED)

def main():
    print("Prog start")
    while True: 
        try:       
            print(axis_queue.get())
            if not axis_queue.empty():
                print(axis_queue.qsize())
                for _ in range(axis_queue.qsize()-1):
                    data = axis_queue.get_nowait()

                if data == False:
                    dled.progLed(Status.FILE_TRANSMITT,LEDS.DATALED)
                    data=[0,0,0,-1,0,0,-1]

                servoRL.setVal((data[3] + data[6]*-1)/2)
                throtleR.setVal(data[2]*-1)
                throtleL.setVal(data[2]*-1)
                servoUDL.setVal((data[4]*-1 + data[5])/2)
                servoUDR.setVal((data[4]*-1 + data[5]*-1)/2)   
                print(data)
                            
        except KeyboardInterrupt:
            dled.clear()
            tx.join()
            db.join()
            for i in servos:
                i.stop()
            sys.exit()
                  
        except Exception as e:
            print(e)
            dled.clear()
            dled.progLed(Status.UNKNOWNERROR,LEDS.PROGLED)
            
        else:
            dled.progLed(Status.NOSTATE,LEDS.HEALTHLED)
            dled.progLed(Status.READY,LEDS.PROGLED)
            
        finally:
            dled.clear()
            

if __name__ ==  "__main__":        
    main()      

