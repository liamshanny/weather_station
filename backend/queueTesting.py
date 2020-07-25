from queue import SimpleQueue
import time
import datetime
import board
import busio
import subprocess
import umsgpack
import adafruit_lps35hw
import adafruit_si7021
from smbus import SMBus as smb
from si7021 import Si7021 as si

#bus and hardware descriptors

i2c = busio.I2C(board.SCL, board.SDA)
lps35hw = adafruit_lps35hw.LPS35HW(i2c)
si7021 = si(smb(1))


commandQueue = SimpleQueue() #queue to store weather messages in

def logData():
    data = {}
    data["timeStamp"] = int(datetime.datetime.now().timestamp()) #seconds since the epoch rounded down
    data["lpsTemp"] = lps35hw.temperature
    data["lpsPressure"] = lps35hw.pressure
    siHum, siTemp = si7021.read()
    data["siTemp"] = siTemp
    data["relativeHumidity"] = siHum
    data["lightData"] = {"r":255, "g":255, "b":255, "intensity":255}
    data["rainFall"] = .1
    data["windData"] = {"speed":2.2, "direction":"nw"}
    data["lastIp"] = getIp()
    command = {"command":"sendStandardData", "data":data}
    print(command)
    command = umsgpack.packb(command)
    commandQueue.put(command)

def getIp():
    out = subprocess.check_output(["ifconfig", "wwan0"]).decode("utf-8")
    start = out.find("broadcast")+10
    subOut = out[start:out.find("\n",start)]

for x in range(5):
    logData()
    time.sleep(5)
print(commandQueue.qsize)