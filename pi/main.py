import time
import requests
import subprocess
import dataLogging
import pigpio
from queue import SimpleQueue
from sensorCollection import sensorPackage
sampleInterval = 5 #seconds between samples
sampleCount = 0

def main():
    #check for 4g connection
    #init code
    sensors = sensorPackage(27, ['a','c'])
    sensorQueue = SimpleQueue()
    while(1):
        data = dataLogging.logData(sensorQueue, sensors)
        #output = data['data']
        #sensors.cam.captureAll()
        headers = {"content-type": "application/x-msgpack"}
        cert = ('../backend/certs/user.crt', '../backend/certs/user_unencrypted.key')
        #data = sensorQueue.get()
        #print(data)
        r = requests.post('https://108.7.77.7/api/v1/full-send', data=data, headers=headers, cert=cert, verify=False)
        print(r.reason)
        time.sleep(sampleInterval)
