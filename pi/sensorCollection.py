import adafruit_lps35hw
import adafruit_si7021
import pigpio
from smbus import SMBus as smb
import busio
import board
from si7021 import Si7021 as si
import as3935
from camera import multiCam

class sensorPackage:

    bus = 1
    as3935Addr = 0x03


    def __init__(self, asIntPin, enabledCams):
        #bus and hardware descriptors
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.lps35hw = adafruit_lps35hw.LPS35HW(self.i2c)
        self.si7021 = si(smb(self.bus))
        #maybe add delay here?
        #self.lightningSensor = as3935.AS3935(asIntPin, self.bus, self.as3935Addr) #this uses a pigpio socket
        self.pi = pigpio.pi() #for general gpio, may not end up needing this
        self.cam = multiCam(enabledCams, self.pi,[1]) #init camera board with a=fisheye, c = ir (this could go in main?)



    @property
    def lpsPressure(self):
        try:
            return self.lps35hw.pressure
        except Exception as e:
            print("error reading lps pressure")
            print(e)
            return -1

    @property
    def lpsTemperature(self):
        try:
            return self.lps35hw.temperature
        except:
            print("error reading lps temp")
            return -273 #-1 is a valid value for temp in c, so 0 kelvin it is

    @property
    def siData(self):
        try:
            siHum, siTemp = self.si7021.read()
            return (siHum, siTemp)
        except Exception as e:
            print("error reading from si7021")
            print(e)
            return (-1, -273)
