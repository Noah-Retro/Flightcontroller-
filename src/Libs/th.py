import threading
import time
import keyboard
from controller import PS4Controller

global controller
controller = PS4Controller()


global y #making a variable acceble through all threads -> controller object for example
y = 0
def thread_function(name):
    global y
    print("Thread %s: starting", name)
    while True:
        time.sleep(1/(index+1))
        print("Thread %s: finishing", name)
        print(y)
        y = name

if __name__ == "__main__":
    
    controller.init()
    x = threading.Thread(target=controller.listen, daemon=True)
    x.start()
    #threads:list[threading.Thread] = []
    #for index in range(3):
    #    x = threading.Thread(target=thread_function, args=(index,), daemon=True)
    #    threads.append(x)
    #    x.start()
    #for index, thread in enumerate(threads):
    #    thread.join()
    while not keyboard.is_pressed("q"):
        print(controller.axis_data)