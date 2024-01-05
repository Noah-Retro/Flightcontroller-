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
    
    
    
    
    
    
    
    
    
    
    
    
    while True:
        if not controllerQueue.empty():
            
            for _ in range(controllerQueue.qsize()-1):
                controllerData = controllerQueue.get_nowait()
        
        if len(controllerData)>0:
            if controllerData[0][0]:
                controller.rumble(low_frequency=0.5,high_frequency=1,duration=0)
            else:
                controller.stop_rumble()
                
                
        
                
        
        
        
                
        
                        
        