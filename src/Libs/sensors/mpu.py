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
    
    @property
    def magVals(self):
        self.imu.readSensor()
        self.imu.computeOrientation()
        return self.imu.MagVals
    
    def calliberateAccelerometer(self):
        """Caliberate Accelerometer by positioning it in 6 different positions

This function expects the user to keep the imu in 6 different positions while caliberation. It gives cues on when to change the position. It is expected that in all the 6 positions, at least one axis of IMU is parallel to gravity of earth and no position is same. Hence we get 6 positions namely -> +x, -x, +y, -y, +z, -z.
        """
        self.imu.caliberateAccelerometer()
        
    def calliberateGyro(self):    
        self.imu.caliberateGyro()
        
    def calliberateMag(self):
        self.imu.caliberateMagApprox()

if __name__ == '__main__':
    sens = MPU_9250()
    sens.run()
    
    while True:
        print("Accelometer ",sens.accelVal)
        print("Gyro ", sens.gyroVal)
        print(f"Roll: {sens.roll}, Pitch: {sens.pitch}, Yaw: {sens.yaw}")
        print("Mag vals: ",sens.magVals)
    """
    Output:
    Accelometer  [-0.18675724 -0.13408212 -9.48631028]
    Gyro  [ 0.00196677 -0.0028696   0.00085888]
    Roll: -178.7302714712781, Pitch: 0.8388532267318494, Yaw: nan
    Mag vals:  [nan nan nan]
    """