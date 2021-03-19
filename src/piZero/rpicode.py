import os, sys, digitalio, board, busio, time
from adafruit_lc709203f import LC709203F
import adafruit_bmp3xx as atmosphericSensor
import adafruit_lis3mdl.LIS3MDL as LIS3MDL
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33



i2c = busio.I2C(board.SCL, board.SDA)


# create IMU object
accelGyro = LSM6DS33(i2c)
magnetometer = LIS3MDL(i2c)

# create atmospheric sensor object
airSensor = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# may remove the battery sensor at later date
battSensor = LC709203F(i2c)


# initialize GPS object
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False) 
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")


while True:
    pass
# airSensor.pressure
# airSensor.temperature
# airSensor.altitude
# airSensor.sea_level_pressure = ???
