from picamera import PiCamera
import pigpio
import datetime

class multiCam():

    camSelectionPins = {"a": [0,0,1], "b":[1,0,1], "c": [0,1,0], "d":[1,1,0]}
    camAddr = {"a": 4, "b":5, "c": 6, "d":7}



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


    def captureAll(self):
        i2c = self.pi.i2c_open(1, 0x70)
        for camera in self.enabled:
            try:
                self.pi.i2c_write_device(i2c, [0, self.camAddr[camera]])
            except pigpio.error:
                print("error with i2c write, trying again")
                self.pi.i2c_write_device(i2c, [0, self.camAddr[camera]])
            self.pi.write(4, self.camSelectionPins[camera][0])
            self.pi.write(17, self.camSelectionPins[camera][1])
            self.pi.write(18, self.camSelectionPins[camera][2])
            timestamp = datetime.datetime.now().time() #get time for timestamp
            captureString = "/home/pi/weatherStation/photos/camera_"+camera+"/"+str(timestamp.hour)+":"+str(timestamp.minute)+":"+str(timestamp.second)+".jpg"
            try:
                self.cam.capture(captureString, quality=100)  # minimize any compression
            except picamera.exc.PiCameraRuntimeError:
                self.cam.capture(captureString, quality=100)  #this error usually happens on the first attempt to capture, always works on second try and never recurs
        self.pi.i2c_close(i2c)
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
