import adafruit_lps35hw
import adafruit_si7021
import Adafruit_ADS1x15
import isl29125
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
        #bus and hardware descriptors1
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.lps35hw = adafruit_lps35hw.LPS35HW(self.i2c)
        self.si7021 = si(smb(self.bus))
        #maybe add delay here?
        #self.lightningSensor = as3935.AS3935(asIntPin, self.bus, self.as3935Addr) #this uses a pigpio socket
        self.pi = pigpio.pi() #for general gpio, may not end up needing this
        #self.cam = multiCam(enabledCams, self.pi,[1]) #init camera board with a=fisheye, c = ir (this could go in main?)
        self.adc = Adafruit_ADS1x15.ADS1015() #init adc for wind speed+dir sensor, light intensity 
        self.rgbSensor = isl29125.ISL29125([0x0d,0x3f,0])




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
        except Exception as e:
            print("error reading lps temp")
            print(e)
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

    @property
    def lightIntensity(self):
        try:
            output = self.adc.read_adc(0)
            print(output)
            voltage = output * .002 #LSB=2mV with gain=1
            #print(voltage)
            current = voltage/10000 #sensor breakout board uses 10k resistor
            lux = (current/(1/10**5))/20 #data sheet says 10uA/20lux, so use that as cal value and divide by 20 for accuraccy
            #print(lux)
            return lux
        except:
            print("error reading adc")
            return -1