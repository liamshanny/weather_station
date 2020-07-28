from queue import SimpleQueue
import time
import datetime
import subprocess
import umsgpack


commandQueue = SimpleQueue() #queue to store weather messages in

def logData(queue, sensors):
    data = {}
    data["timeStamp"] = int(datetime.datetime.now().timestamp()) #seconds since the epoch rounded down
    data["lpsTemp"] = sensors.lpsTemperature
    time.sleep(.1)
    data["lpsPressure"] = sensors.lpsPressure
    time.sleep(.1)
    siHum, siTemp = sensors.siData
    data["siTemp"] = siTemp
    data["relativeHumidity"] = siHum
    data["lightData"] = {"r":255, "g":255, "b":255, "intensity":255}
    data["rainFall"] = .1
    data["windData"] = {"speed":2.2, "direction":"nw"}
    data["lastIp"] = getIp()
    command = {"command":"sendStandardData", "data":data}
    print(data)
    command = umsgpack.packb(command)
    commandQueue.put(command)
    return command

def getIp():
    out = subprocess.check_output(["ifconfig", "wwan0"]).decode("utf-8")
    index = out.find("mtu") #just in case flags has broadcast
    start = out.find("broadcast",index)
    if start == -1:
        print("using eth0")
        out = subprocess.check_output(["ifconfig", "eth0"]).decode("utf-8")
        index = out.find("mtu")
        start = out.find("broadcast", index)
    subOut = out[start+10:out.find("\n",start+10)]
    return subOut
