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

headers = {"content-type": "application/x-msgpack"}
cert = ('../backend/certs/user.crt', '../backend/certs/user_unencrypted.key')

def main():
    #check for 4g connection
    #init code
    sensors = sensorPackage(27, ['a','c'])
    dataQueue = SimpleQueue()
    logQueue = SimpleQueue()
    
    while(1):
        for x in range(6):
            data = dataLogging.logData(dataQueue, sensors)
            #output = data['data']
            #sensors.cam.captureAll()
            
            #data = sensorQueue.get()
            #print(data)
            dataQueue.put(data)
            time.sleep(sampleInterval)
        
        if logQueue.empty() == False:
            #try to make a single post request and test 
            data = logQueue.get()
            r = sendData(data)
            if not(r.ok):
                logQueue.put(data) #request failed, store it for later
            else:
                #this loop is shit and assumes the server is back for good once it is back, change later or else. Purely to test basic queue implementation if power goes tomorrow
                data = logQueue.get()
                while logQueue.empty() == False:
                    r = sendData(data)    

        while dataQueue.empty() == False:
            try:
                data = dataQueue.get(timeout=.5)
                r = sendData(data)
                if not(r.ok):
                    print("error talking to server")
                    logQueue.put(data) #request failed, store it for later
            except Exception as e:
                print(e)

def sendData(data):
    r = requests.post('https://weather.shanny.tools/api/v1/full-send', data=data, headers=headers, cert=cert, verify=False)
    return r


main()
