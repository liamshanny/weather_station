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

testWeatherData = {
    "startTime": 1595382642,
    "sampleInterval": 60,
    "lpsTemp": [40.3213, 23.54],
    "siTemp": [40.3213, 54.43],
    "relativeHumidity": [60.60, 30.00],
    "pressure": [123.321, 232.0932],
    "lightData": [{"r": 5451.5, "g": 5456.516, "b": 15.1, "intensity": 5}, {"r": 5451.5, "g": 5456.516, "b": 15.1,
                                                                            "intensity": 5}],
    "rainFall": [34234.3423, 4382.232],
    "windData": [{"speed": 54156.5416, "direction": "north"}, {"speed": 54156.5416, "direction": "north"}],
    "lastIp": "10.1.10.54"
    }

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
r = requests.post('https://108.7.77.7/api/v1/full-send', data=data, headers=headers, cert=cert, verify=False)
print(r.reason)

