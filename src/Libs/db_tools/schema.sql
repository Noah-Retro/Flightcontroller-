CREATE TABLE IF NOT EXISTS mpu(
    id INTEGER PRIMARY KEY,
    gyro_x FLoat,
    gyro_y FLoat,
    gyro_z FLoat,
    accelometer_x float,
    accelometer_y float,
    accelometer_z float,
    mag_x float,
    mag_y float,
    mag_z float,
    roll FLOAT,
    pitch FLOAT,
    yaw FLOAT,
    fligth INTEGER,
    track timestamp
);
