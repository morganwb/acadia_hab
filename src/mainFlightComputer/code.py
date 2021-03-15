print("Welcome to the Acadia Launch Console v 0.2")
print("="*20)
# import all libraries
import time, array, math, board, neopixel, busio, digitalio, storage
import adafruit_bmp280
import adafruit_lis3mdl
import adafruit_lsm6ds.lsm6ds33
import adafruit_sht31d
import adafruit_gps
import adafruit_sdcard
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
i2c = board.I2C()
DIO = digitalio.DigitalInOut
print("Initialized all libraries")

# What mode are we running in?
# 0 Flight (all systems online, all-up)
# 1 GPS/Sensor data collection testing (no radios)
# 2 BLE testing block (testing communications between pi/particle)

MODE = 1


# initialize neopixel as sensor to indicate startup status
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel[0] = (255, 0, 0)

# initialize the other LEDs on the board
blue_led = digitalio.DigitalInOut(board.BLUE_LED)
#red_led = digitalio.DigitalInOut(board.RED_LED)
blue_led.direction = digitalio.Direction.OUTPUT
#red_led.direction = digitalio.Direction.OUTPUT
print("[OK] LED objects")

# initialize all sensors
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
lis3mdl = adafruit_lis3mdl.LIS3MDL(i2c)
lsm6ds33 = adafruit_lsm6ds.lsm6ds33.LSM6DS33(i2c)
sht31d = adafruit_sht31d.SHT31D(i2c)
print("[OK] nRF52840 onboard sensor objects")


# cutdownSafe *SAFES* the system. this should be connected to UNSET on the latching wing
cutdownSafe = DIO(board.D13)
cutdownSafe.direction = digitalio.Direction.OUTPUT
cutdownSafe.value = True
time.sleep(0.1)
cutdownSafe.value = False
# cutdownInit *INITIATES* the system. this should be connected to SET on the latching wing
cutdownInit = DIO(board.D12)
cutdownInit.direction = digitalio.Direction.OUTPUT
cutdownInit.value = False
print("[OK] Cutdown objects")

# initialize Bluetooth Low Energy (BLE)
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
print("[OK] Bluetooth low energy objects initialized")

# initialize GPS featherwing
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=True)
gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b"PMTK220,1000")
print("[OK] GPS objects loaded")

# initialize SPI and SD card module
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DIO(board.D10)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
print("[OK] SD card connected")

# switch neopixel to blue once all modules are initialized
pixel[0] = (0, 0, 255)

print("beginning GPS connection sequence")
# get GPS fix
while not gps.has_fix:
    gps.update()
    time.sleep(0.1)
    #print(gps.has_fix)

print("[OK] Good GPS connection.")
print("Latitude: " + str(gps.latitude))
print("Latitude: " + str(gps.longitude))
print("Satellites: " + str(gps.satellites))
print("GPS Altitude: " + str(gps.altitude_m))
print("ENDING GPS TEST SEQUENCE")

#def cutDown(alt, cutdownAlt):
 #   cutdownInit.value = True
  #  while alt > cutdownAlt:
   #     time.sleep(1)

if MODE == 2:
    while True:
        ble.start_advertising(advertisement)
        print("Waiting to connect")
        while not ble.connected:
            pass
        print("Connected")
        while ble.connected:
            #s = uart.readline()
            #if s:
            #    print(s)
            #xyz = str(gps.latitude) + ":" + str(gps.longitude) + ":" + str(gps.altitude_m)
            xyz = str(gps.latitude)
            uart.write(xyz.encode("utf-8"))
            time.sleep(1)

# open file!

if MODE == 1:
    with open("/sd/testdata.txt", "a") as fh:
        fh.write(str("restarted at" + str(time.time())) + " \n")
    while True:
        data = [str(bmp280.temperature),
        str(bmp280.pressure),
        str(bmp280.altitude),
        str(sht31d.relative_humidity),
        str(lis3mdl.magnetic),
        str(lsm6ds33.acceleration),
        str(lsm6ds33.gyro),
        str(gps.latitude),
        str(gps.longitude),
        str(gps.altitude_m)
        ]
        with open("/sd/testdata.txt", "a") as fh:
            fh.write(str(data) + " \n")
        print("file write successful!")
        gps.update()
        time.sleep(5)
        pixel[0] = (0, 255, 0)


if MODE ==0:
    while True:
        pass























