import smbus
import datetime

from imusensor.MPU9250 import MPU9250
import pandas as pd

class MPU_9250():
    def __init__(self,address:int=0x68,bus:int=1) -> None:
        self.address = address
        self.bus = smbus.SMBus(bus)
        self.imu = MPU9250.MPU9250(self.bus, self.address)
        self.imu.begin()
        self.dataFrame_ = pd.DataFrame()
      
        

    def dataFrame(self)->pd.DataFrame:
        self.imu.readSensor()
        data = {
            "Timestamp":datetime.datetime.now(),
            "Acceleration_X":self.imu.AccelVals[0],
            "Acceleration_Y":self.imu.AccelVals[1],
            "Acceleration_Z":self.imu.AccelVals[2],
            "Gyro_X":self.imu.GyroVals[0],
            "Gyro_Y":self.imu.GyroVals[1],
            "Gyro_Z":self.imu.GyroVals[2]            
        }
        return data
       
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
        print(sens.dataFrame)
 