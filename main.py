import src.Libs.autoupdate as ap
import src.Libs.controller as controller
from sys import platform
import os
from threading import Thread

try:
    if platform == "linux":
        ap.update(os.path.dirname(os.path.abspath(__file__)))
except Exception as e:
    raise e

c = controller.PS4Controller()
c.init()

if __name__ == '__main__':
    threads = []
    controllerThread = Thread(target=c.listen,daemon=True)
    threads.append(controllerThread)
    
    for thread in threads:
        thread.start()
        
    while True:
        print(c.button_data,c.axis_data,c.hat_data)




    

