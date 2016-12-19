﻿import RPi.GPIO as GPIO
import time
import datetime
import threading 
from threading import Thread
from laser import getLaserDistArr
GPIO.setwarnings(False)

con=threading.Condition()
stoper=0


cosmos=(1,2,-1,-2) #1=y,2=x
dir=0

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)
GPIO.setup(20,GPIO.IN)

counterleft=0
counterright=0
counterleft_limit=0
counterright_limit=0

def getDist():
    GPIO.setmode(GPIO.BCM)
    TRIG = 23
    ECHO = 22
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance
def stop():
    GPIO.setmode(GPIO.BCM)
    A1 = 26
    A2 = 27
    B1 = 24
    B2 = 25
    GPIO.setup(A1,GPIO.OUT)
    GPIO.setup(A2,GPIO.OUT)
    GPIO.setup(B1,GPIO.OUT)
    GPIO.setup(B2,GPIO.OUT)
    GPIO.output(A1, 0)
    GPIO.output(A2, 0)
    GPIO.output(B1, 0)
    GPIO.output(B2, 0)
    GPIO.cleanup()
    return
def addleft(channel):
	global counterleft,con
	counterleft+=1
	if counterleft>=counterleft_limit:
		GPIO.setmode(GPIO.BCM)
		GPIO.output(26,True)
		GPIO.output(27,True)
		con.acquire()
		print "left finito"
		print datetime.datetime.now()-stoper
		con.notify()
		con.release()
		GPIO.remove_event_detect(channel)
def turnright():
	global counterleft
	global counterright
	global con
	global counterright_limit
	global counterleft_limit
	global dir
	globalinit();

	counterright_limit=58
	counterleft_limit=58

	GPIO.setmode(GPIO.BCM)
	A1 = 26
	A2 = 27
	B1 = 24
	B2 = 25
	GPIO.setup(A1,GPIO.OUT)
	GPIO.setup(A2,GPIO.OUT)
	GPIO.setup(B1,GPIO.OUT)
	GPIO.setup(B2,GPIO.OUT)
	GPIO.output(A1, True)
	GPIO.output(A2, False)
	GPIO.output(B1, False)
	GPIO.output(B2, True)
	GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
	GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)

	con.acquire()
	while True:
	 con.wait()
	 if counterleft>=counterleft_limit and counterright>=counterright_limit:
	  break
	con.release()
	dir=(dir+1)%4

	    
def turnleft():
	global counterleft
	global counterright
	global con
	global counterright_limit
	global counterleft_limit
	global dir
	globalinit()
	counterright_limit=56
	counterleft_limit=56
	GPIO.setmode(GPIO.BCM)
	A1=26
	A2=27
	B1=24
	B2=25
	GPIO.setup(A1,GPIO.OUT)
	GPIO.setup(A2,GPIO.OUT)
	GPIO.setup(B1,GPIO.OUT)
	GPIO.setup(B2,GPIO.OUT)
	GPIO.output(A1, True)
	GPIO.output(A2, False)
	GPIO.output(B1, False)
	GPIO.output(B2, True)
	GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
	GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
	con.acquire()
	while True:
		print "Sleep"
		con.wait()
		print "counters in turn: left "+str(counterleft)+" right"+str(counterright)
		if counterleft>=counterleft_limit  and counterright>=counterright_limit:
			break
	counterleft=0
	counterright=0
	con.release()
	dir=(dir-1)%4
def addright(channel):
	global counterright,con
	counterright+=1
	if counterright>=counterright_limit:
		GPIO.setmode(GPIO.BCM)
		GPIO.output(24,True)
		GPIO.output(25,True)
		con.acquire()
		con.notify()
		print "right finito"
		print datetime.datetime.now()-stoper
		con.release()
		GPIO.remove_event_detect(channel)

def moveForward():
	global counterleft
	global counterright
	global con
	global counterright_limit
	global counterleft_limit
	global stoper
	globalinit()
	counterright_limit=100
	counterleft_limit=100
	GPIO.setmode(GPIO.BCM)
	GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
	GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
	A1 = 26
	A2 = 27
	B1 = 24
	B2 = 25
	GPIO.setup(A1,GPIO.OUT)
	GPIO.setup(A2,GPIO.OUT)
	GPIO.setup(B1,GPIO.OUT)
	GPIO.setup(B2,GPIO.OUT)
	stoper=datetime.datetime.now()
	GPIO.output(A1, False)
	GPIO.output(A2, True)
	GPIO.output(B1, False)
	GPIO.output(B2, True)
	con.acquire()
	while True:
	 con.wait()
	 if counterleft>=counterleft_limit and counterright>=counterright_limit:
	  break
	con.release()
def turnsens():
	GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
	GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
	globalinit()
	global counterright_limit
	global counterleft_limit
	counterleft_limit=1000
	counterright_limit=1000
def globalinit():
	global counterleft
	global counterright
	global counterright_limit
	global counterleft_limit
	counterleft=0
	counterright=0
	counterleft_limit=0
	counterright_limit=0
def turn360():
	for x in range(0,4):
		time.sleep(1)
		turnleft()
def movenone():
	GPIO.setmode(GPIO.BCM)
	A1 = 26
	A2 = 27
	B1 = 24
	B2 = 25
	GPIO.setup(A1,GPIO.OUT)
	GPIO.setup(A2,GPIO.OUT)
	GPIO.setup(B1,GPIO.OUT)
	GPIO.setup(B2,GPIO.OUT)
	GPIO.output(A1, False)
	GPIO.output(A2, True)
	GPIO.output(B1, False)
	GPIO.output(B2, True)

def move30cm():    
	moveForward()
	time.sleep(2)
	moveForward()
	time.sleep(2)

def cali():
    GPIO.setmode(GPIO.BCM)
    R1 = 18 # RELAY PIN	
    GPIO.setup(R1,GPIO.OUT)
    res = [0]*10
    realDist = [285]*10
    for x in range(10):
            GPIO.output(R1, True) # laser on
            res[x] = getLaserDistArr()
            #time.sleep(1)
            realDist[x] = realDist[x]-60*x
		    #here some function that will take picture
            GPIO.output(R1, False) #laser off
            move30cm()
##clac here

def main():
	#turnsens()
	#turnleft()
	#turn360()
	#moveForward()
	#movenone()
	#print "end forward"
	#time.sleep(3)
	#print "after sleep"
	#turnleft()
	#stop()
	cali()
	while True:
	 pass

main()