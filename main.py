import src.Libs.autoupdate as ap
import src.Libs.controller as controller

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
c = controller.PS4Controller()
c.init()

if __name__ == '__main__':
    threads = []
    controllerThread = Thread(target=c.listen,daemon=True,args=(controllerQueue,))
    threads.append(controllerThread)
    controllerData = None
    
    for thread in threads:
        thread.start()
        
    while True:
        print(controllerQueue.empty())
        if not controllerQueue.empty():
            controllerData = controllerQueue.get(block=False)
        print(controllerData)
        
        
        



    

