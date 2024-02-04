from collections.abc import Callable, Iterable, Mapping
from math import sqrt
import math
import time
from typing import Any

from numpy import roots,clip,interp


def timer(func):
    def wrapper(*args,**kwargs):
        start = time.perf_counter_ns()
        func(*args,**kwargs)
        end = time.perf_counter_ns()
        print(f"Delta: {(end-start)/1000000}ms")
    return wrapper
        
@timer
def test_file_send():
    import math
    with open("Flightcontroller-/src/settings/transmitt.json") as data:
        b = bytes(data.read(),'utf-8')
    c = []
    for i in range(int(math.ceil(len(b)/31))):
        s = list(b[i*31:i*31+31])
        s[:0]=[0x03]
        c.append(s) #Send data for a file
    
    g:bytes=b'0'
    for i in c: #recever side
        i.pop(0)
        for k in i:
            k:int
            g+=k.to_bytes()
    g = g[1:].decode()
    print(g)

@timer
def test_visualization():
    from db_tools import DbHandler
    from gui import VisualizationHandler
    db = DbHandler()
    vsh = VisualizationHandler()
    db.storeTestData(100,1)
    df = db.load_test_data()
    fig = vsh.plot_3d_coordinates(df).show()
    vsh.plot_2d_path_on_map(df).show()        

    
import multiprocessing as mp
import threading as th
def run(num):
        start = time.process_time_ns()
        list = [x for x in range(500000)]
        for i in list:
            i = i**2//3
        for i in list:
            i = i**1000
        stop = time.process_time_ns()
        delta = stop-start
        print(f"elapsed time {num}:\n delta:{delta/1000000} start:{start/1000000} stop:{stop/1000000}\n")

def test_process_thread():
    bp1 = th.Thread(target=run,args=(1,))
    bp2 = th.Thread(target=run,args=(2,))
    bp3 = th.Thread(target=run,args=(3,))
    bp1.start()
    bp2.start()
    bp3.start()
    bp4 = mp.Process(target=run,args=(4,),name="Big Data Process")
    bp5 = mp.Process(target=run,args=(5,))
    bp6 = mp.Process(target=run,args=(6,))
    bp4.start()
    bp5.start()
    bp6.start()

def upRot():
    l2 = [(math.sin(x),math.cos(x))for x in range(360)]
    lr = l2
    #List from -1 to 1 in 0.01 steps
    el=[]
    print(l2[0])
    for lift,rotation in lr:
        res = (rotation+lift)/2
        el.append(res)
        print(f"Das Resultat ist: {res} von {rotation} und {lift} Grad: {0}")
    print(min(el),max(el))



if __name__ == "__main__":
    maxw = 2000
    minw= 950
    zero = 0.4
    for i in range(200):
        xn = (((i-100)/100))
        print(interp(xn,[-1,1-zero],[950,2000]))
    print(interp(0,[-1,1-zero],[950,2000]))
        

        
        

    



   

    

