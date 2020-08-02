from picamera import PiCamera
import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
import pigpio
import datetime
from smbus import SMBus as smb
import os

class multiCam():

    camSelectionPins = {"a": [0,0,1], "b":[1,0,1], "c": [0,1,0], "d":[1,1,0]}
    camAddr = {"a": 4, "b":5, "c": 6, "d":7}
    i2cAddr = 0x70


    def __init__(self, enabledCameras, pi, cameraParams):
        self.cam = PiCamera()
        self.cam.resolution = (3280, 2464) #max resolution, fuck data caps
        self.enabled = enabledCameras #used for capture all
        self.pi = pi #have an instance of the pigpio socket for i2c and gpio control
        #camera select outputs
        self.pi.set_mode(4, pigpio.OUTPUT)
        self.pi.set_mode(17, pigpio.OUTPUT)
        self.pi.set_mode(18, pigpio.OUTPUT)

        self.pi.set_mode(22, pigpio.OUTPUT)
        self.pi.set_mode(23, pigpio.OUTPUT)
        self.pi.set_mode(9, pigpio.OUTPUT)
        self.pi.set_mode(25, pigpio.OUTPUT)

        #mystery IO that has to be high to enable the camera
        self.pi.write(22, 1)
        self.pi.write(23, 1)
        self.pi.write(9, 1)
        self.pi.write(25, 1)

        #self.i2c = smb(1) #use SMB for i2c, pigpio didn't play nicely with the shitshow of libs


    def captureAll(self):

        for camera in self.enabled:
            try:
                i2c = "i2cset -y 1 0x70 0x00 0x0" +str(self.camAddr[camera])
                os.system(i2c)
                #self.i2c.write_byte_data(self.i2cAddr, 0, self.camAddr[camera])
            except OSError:
                print("error")
                #self.i2c.write_byte_data(self.i2cAddr, 0, self.camAddr[camera])
            self.pi.write(4, self.camSelectionPins[camera][0])
            self.pi.write(17, self.camSelectionPins[camera][1])
            self.pi.write(18, self.camSelectionPins[camera][2])
            timestamp = datetime.datetime.now().time() #get time for timestamp
            captureString = "/home/pi/weatherStation/photos/camera_"+camera+"/"+str(timestamp.hour)+":"+str(timestamp.minute)+":"+str(timestamp.second)+"_"+camera+".jpg"
            try:
                self.cam.capture(captureString, quality=100)  # minimize any compression
            except picamera.exc.PiCameraRuntimeError:
                self.cam.capture(captureString, quality=100)  #this error usually happens on the first attempt to capture, always works on second try and never recurs
        return captureString #idk this may be unnecessary

    def capture(self, camSelection):
        print("capture single image")
        if camSelection in self.enabled:
            i2c = self.pi.i2c_open(1, 0x70)
            try:
                self.pi.i2c_write_device(i2c, [0, self.camAddr[camSelection]])
            except pigpio.error:
                print("error with i2c write, trying again")
                self.pi.i2c_write_device(i2c, [0, self.camAddr[camSelection]])
            self.pi.write(4, self.camSelectionPins[camSelection][0])
            self.pi.write(17, self.camSelectionPins[camSelection][1])
            self.pi.write(18, self.camSelectionPins[camSelection][2])
            timestamp = datetime.datetime.now().time()  # get time for timestamp
            captureString = "/home/pi/weatherStation/photos/camera_" + camSelection +"/capture"+ str(timestamp.hour) + ":" + str(timestamp.minute) + ".jpg"
            try:
                self.cam.capture(captureString, quality=100)  # minimize any compression
            except picamera.exc.PiCameraRuntimeError:
                self.cam.capture(captureString, quality=100)  # this error usually happens on the first attempt to capture, always works on second try and never recurs
            return captureString
        else:
            return -1
