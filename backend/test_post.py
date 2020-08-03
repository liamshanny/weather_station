import time
import board
import busio
import csv
import adafruit_lps35hw
import adafruit_si7021
from smbus import SMBus as smb
from si7021 import Si7021 as si
import requests
import umsgpack


i2c = busio.I2C(board.SCL, board.SDA)
lps35hw = adafruit_lps35hw.LPS35HW(i2c)
#si7021 = adafruit_si7021.SI7021(i2c)
si7021 = si(smb(1))
lpsTempBuf = []
siTempBuf = []
pressureBuf = []
humBuf = []

testWeatherData = {'command': 'test','data': {'timeStamp': 1595817930, 'lpsTemp': 524.28, 'lpsPressure': -0.043701171875,
                               'siTemp': 23.38866455078125,
                               'relativeHumidity': 49.461883544921875,
                               'lightData': {'r': 255, 'g': 255, 'b': 255, 'intensity': 255},
                               'rainFall': 0.1, 'windData': {'speed': 2.2, 'direction': 'nw'},
                               'lastIp': '169.254.255.255'}}


def logMeasurement():
    lpsTempBuf.append(lps35hw.temperature)
    pressureBuf.append(lps35hw.pressure)
    siHum, siTemp = si7021.read()
    siTempBuf.append(siTemp)
    humBuf.append(siHum)

for x in range(5):
    logMeasurement()
    print("measurement logged")
    time.sleep(60)
    
testWeatherData["lpsTemp"] = lpsTempBuf
testWeatherData["siTemp"] =  siTempBuf
testWeatherData["pressure"] =  siTempBuf
testWeatherData["relativeHumidity"] =  humBuf

data = umsgpack.packb(testWeatherData)
headers = {"content-type": "application/x-msgpack"}
cert = ('certs/user.crt', 'certs/user_unencrypted.key')
r = requests.post('https://weather.shanny.tools/api/v1/full-send', data=data, headers=headers, cert=cert, verify=True)
print(r.reason)

