import time
import picamera
import picamera.array
import cv2
import numpy as np
import math
from scipy import stats
import RPi.GPIO as GPIO
from proxsens import move30cm 
from robotModels import DistConst
GPIO.setwarnings(False)

#Global variables
DistConstArr = np.empty(640,dtype=DistConst)
distH = 5
initialD = 285


#Function to detect laser line from camera and return array of y distances from camera horizon per column
#Since camera resolution is 640*480, an array of 680 values is returned
def getLaserDistArr():
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr') #take a photo
            image = stream.array
            num = (image[...,...,1] > 200) #only marks pixels of bright green color
            y_vals = [np.nan]*640
            for i in range(200,400) :
                x = num[:,i].nonzero()
                if len(x) != 0 :
                    y_vals[i] = abs(np.median(x)-240) #in case of multiple pixles per column, a median of dais pixel is computed
        camera.close()
    return y_vals

def cali():
    GPIO.setmode(GPIO.BCM)
    R1 = 18 # RELAY PIN	
    GPIO.setup(R1,GPIO.OUT)
    pixelDist = []
    theta = np.empty(10) #an array of theta per distance from wall
    theta.fill(initialD) #the array instantaniates as D in cm and than
                         #converted to angle via artctan(h/D)
    for x in range(10):
            GPIO.output(R1, True) # laser on
            pixelDist.append(getLaserDistArr())
            theta[x] = math.atan(distH/(theta[x]-30*x)) #D in cm converted to theta
            GPIO.output(R1, False) #laser off
            print ("ended loop" + str(x))
            #move30cm()
            time.sleep(0.5)
    
    np_pixelDist = np.asarray(pixelDist) #pixelDist matrix converted to numpy matrix - for performance
    #take every column and compute slope and offset from multiple readings
    for i in range(200,400) :
        x = np_pixelDist[:,i] 
        mask = ~np.isnan(x) #mask = ignore any 'nan' values in the matrix
        slope, intercept, r_value, p_value, std_err = stats.mstats.linregress(x[mask],theta[mask])
        DistConstArr[i] = DistConst(slope,intercept) #add computer values to distance constants array
    np.save('consts.txt', DistConstArr)

cali()


'''

#CalcDistCalibration
with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        x = input("system ready")
        camera.capture(stream, format='bgr')
        image = stream.array
        num = (image[...,...,1] > 200)
        y_vals = [0] * 640
        for i in range(640) :
            y_vals[i] = abs(np.median(num[:,i].nonzero())-240)
        dist = abs(y_vals - 240) # distance of dot from center y_axis only
        pixelDist = [0] * 640

        for i in range(640) :
            if DistConsts[i] != 0 :
                pixelDist[i] = y_vals[i]*DistConsts[i].Slope + DistConsts[i].Intercept
            y_vals[i] = abs(np.median(num[:,i].nonzero())-240)        

        
	    # work out distance using D = h/tan(theta)

	    #theta =0.0011450*dist + 0.0154
	    #tan_theta = math.tan(theta)

		#if tan_theta > 0: # bit of error checking
		#obj_dist =  int(5.33 / tan_theta)

	    #print "\033[12;0H" + "the dot is " + str(obj_dist) + "cm  away"s
'''