from src.Libs.gui import App, visualization
from src.Libs.tools.paths import SETTINGS_PATH
from src.Libs.transmition import Tx_Thread
import pygame

from sys import platform
import os
from threading import Thread
from queue import Queue
from collections import deque
import time

pygame.init()

tx = Tx_Thread()
app=App(SETTINGS_PATH)

controllerData = []

if __name__ == '__main__':
    
    app.start()
    tx.start()
    
    while True:
        "maybe at a later state the visualization"
        pass
        

                
                
        
                
        
        
        
                
        
                        
        