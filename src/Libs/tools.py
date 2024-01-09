import json

class Status():
    NOSTATE=[0,0,0]
    BOOTUP=[255,0,0]
    WAITING=[255,255,0]
    READY=[0,255,0]
    UNKNOWNERROR=[255,255,255]
    VOLTAGELOW=[255,0,0]
    I2CERROR=[0,255,0]
    SPIERROR=[0,0,255]
    TRANSMITTERROR=[255,0,0]
    DBERROR=[0,0,255]
    SETTINGSERROR=[0,255,0]
        



class DebugLEDHandler():
    def __init__(pin:int=19):
        #init WS2018 Led strip
        pass

    @staticmethod
    def progLed(state:Status,place:int,pin:int=19):
        #write status to led
        pass

if __name__ == "__main__":
    print(tuple(Status.I2CERROR))