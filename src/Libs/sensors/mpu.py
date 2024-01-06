import os
import sys
import time
import smbus

from imusensor.MPU9250 import MPU9250

class MPU_9250():
    def __init__(self,address:int=0x68,bus:int=1) -> None:
        self.address = address
        self.bus = smbus.SMBus(bus)
        self.imu = MPU9250.MPU9250(self.bus, self.address)
        
    def run(self):
        self.imu.begin()
        
    @property
    def accelVal(self)->list:
        self.imu.readSensor()
        self.imu.computeOrientation()
        return self.imu.AccelVals
    
    @property
    def gyroVal(self)->list:
        self.imu.readSensor()
        self.imu.computeOrientation()
        return self.imu.GyroVals
    
    @property
    def roll(self)->float:
        self.imu.readSensor()
        self.imu.computeOrientation()
        return self.imu.roll
    
    @property
    def pitch(self)->float:
        self.imu.readSensor()
        self.imu.computeOrientation()
        return self.imu.pitch
    
    @property
    def yaw(self)->float:
        self.imu.readSensor()
        self.imu.computeOrientation()
        return self.imu.yaw

if __name__ == '__main__':
    sens = MPU_9250()
    
    while True:
        print("Accelometer ",sens.accelVal)
        print("Gyro ", sens.gyroVal)
        print(f"Roll: {sens.roll}, Pitch: {sens.pitch}, Yaw: {sens.yaw}")
