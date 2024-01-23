import numpy as np

class CustomBrushless():
    def __init__(self,pin:int,clamp_min:float=0,clamp_max:float=2) -> None:
        self.pin = pin
        self.MIN_WIDTH=950
        self.MAX_WIDTH=2100
        self.clamp_min = clamp_min
        self.clamp_max = clamp_max
        self.zero=0

    def scale(self,ins:float):
        res = (self.MAX_WIDTH-self.MIN_WIDTH) * (np.clip((ins+(self.zero)),self.clamp_min,self.clamp_max)/(self.clamp_max)) + self.MIN_WIDTH        
        return int(res)
    
if __name__ == "__main__":
    br = CustomBrushless(26,0,2)
    listd = [-1,-0.5,0,0.5,1]

    for i in listd:
        print(br.scale(i))