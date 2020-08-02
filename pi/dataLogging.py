from queue import SimpleQueue
import json
import time
import datetime
import subprocess
import umsgpack


commandQueue = SimpleQueue() #queue to store weather messages in

def logData(queue, sensors):
    data = {}
    data["timeStamp"] = int(datetime.datetime.now().timestamp()) #seconds since the epoch rounded down
    data["lpsTemp"] = sensors.lpsTemperature
    data["lpsPressure"] = sensors.lpsPressure
    siHum, siTemp = sensors.siData
    data["siTemp"] = siTemp
    data["relativeHumidity"] = siHum
    output = sensors.rgbSensor.rgbVal
    data["lightData"] = {"r":output[0], "g":output[1], "b":output[2], "intensity":sensors.lightIntensity}
    data["rainFall"] = .1
    data["windData"] = {"speed":2.2, "direction":"nw"}
    data["lastIp"] = getIp()
    with open("log.txt", "a") as f:
        f.write(json.dumps(data))
    command = {"command":"sendStandardData", "data":data}
    #print(data)
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
