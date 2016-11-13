#!/usr/bin/python

from __future__ import print_function
from time import sleep
import RPi.GPIO as GPIO

def my_callback(channel):
        global button_ports
        print("Movement!", GPIO.input(channel), channel, button_ports.index(channel))

GPIO.setmode(GPIO.BCM)
button_ports = [14,8,7,15]
for port in button_ports:
        # PUD_OFF (default), PUD_UP or PUD_DOWN
        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        # RISING, FALLING or BOTH
        GPIO.add_event_detect(port, GPIO.FALLING, callback=my_callback, bouncetime=300)
 
# you can continue doing other stuff here
while True:
    sleep(10)