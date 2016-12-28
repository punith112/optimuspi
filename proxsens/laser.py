import RPi.GPIO as GPIO
import picamera
import picamera.array
import numpy as np
from math import tan
import cv2
from cv2 import cv
GPIO.setwarnings(False)

def getPicture():
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.resolution=(640,480)
            camera.capture(stream, format='bgr') #take a photo
            image = stream.array
        camera.close()
    return image

def getLaserDist():
    GPIO.setmode(GPIO.BCM)
    R1 = 18 # RELAY PIN	
    GPIO.setup(R1,GPIO.OUT)
    GPIO.output(R1, True) # laser on
    image = getPicture()
    GPIO.output(R1, False) #laser off
    

    hsv_img = cv2.cvtColor(image, cv.CV_BGR2HSV)

    LASER_MIN = np.array([120, 100, 45.1],np.uint8)
    LASER_MAX = np.array([120, 100, 100],np.uint8)

    frame_threshed = cv2.inRange(hsv_img, LASER_MIN, LASER_MAX)

    #cv.InRangeS(hsv_img,cv.Scalar(5, 50, 50),cv.Scalar(15, 255, 255),frame_threshed)    # Select a range of yellow color
    src = cv.fromarray(frame_threshed)
    #rect = cv.BoundingRect(frame_threshed, update=0)

    leftmost=0
    rightmost=0
    topmost=0
    bottommost=0
    temp=0
    laserx = 0
    lasery = 0
    for i in range(src.width):
        col=cv.GetCol(src,i)
        if cv.Sum(col)[0]!=0.0:
            rightmost=i
            if temp==0:
                leftmost=i
                temp=1
    for i in range(src.height):
        row=cv.GetRow(src,i)
        if cv.Sum(row)[0]!=0.0:
            bottommost=i
            if temp==1:
                topmost=i
                temp=2

    laserx=cv.Round((rightmost+leftmost)/2)
    lasery=cv.Round((bottommost+topmost)/2)
    #return (leftmost,rightmost,topmost,bottommost)
    return laserx, lasery