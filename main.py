import src.Libs.autoupdate as ap
import src.Libs.controller as controller

import pprint
from sys import platform
import os
from threading import Thread
from queue import Queue


try:
    if platform == "linux":
        ap.update(os.path.dirname(os.path.abspath(__file__)))
except Exception as e:
    raise e

controllerQueue = Queue()
c = controller.PS4Controller(controllerQueue)
c.init()

if __name__ == '__main__':
    threads = []
    controllerThread = Thread(target=c.listen,daemon=True)
    threads.append(controllerThread)
    
    for thread in threads:
        thread.start()
        
    while True:
        data = controllerQueue.get()
        pprint.pprint(data)
        




    

