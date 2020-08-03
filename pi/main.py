import time
import urllib3
import requests
import subprocess
import dataLogging
import pigpio
from queue import SimpleQueue
from sensorCollection import sensorPackage
sampleInterval = 10 #seconds between samples
sampleCount = 0

urllib3.disable_warnings()

def main():
    #check for 4g connection
    #init code
    sensors = sensorPackage(27, ['a','c'])
    dataQueue = SimpleQueue()
    logQueue = SimpleQueue()
    headers = {"content-type": "application/x-msgpack"}
    cert = ('../backend/certs/user.crt', '../backend/certs/user_unencrypted.key')
    while(1):
        for x in range(6):
            data = dataLogging.logData(dataQueue, sensors)
            #output = data['data']
            #sensors.cam.captureAll()
            
            #data = sensorQueue.get()
            #print(data)
            dataQueue.put(data)
            time.sleep(sampleInterval)
        
        while dataQueue.empty() == False:
            try:
                data = dataQueue.get(timeout=.5)
                r = requests.post('https://weather.shanny.tools/api/v1/full-send', data=data, headers=headers, cert=cert, verify=False)
                print(r.reason)
            except Exception as e:
                print(e)
main()
