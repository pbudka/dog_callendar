#!/usr/bin/python

# if PI is true then LCD display and Buttons are used
PI = False

if PI:
    from print_lcd import printout, initprint
    import RPi.GPIO as GPIO
    button_ports = [14,8,7,15]
else:
    import msvcrt
    from print_terminal import printout, initprint

from DogWalker import DogWalker

def buttonPressed(channel):
    global button_ports
#    print("Button:",  button_ports.index(channel))
    processChar(button_ports.index(channel))

def initButtons():
    global button_ports, buttonPressed
    GPIO.setmode(GPIO.BCM)
    for port in button_ports:
        # PUD_OFF (default), PUD_UP or PUD_DOWN
        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        # RISING, FALLING or BOTH
        GPIO.add_event_detect(port, GPIO.FALLING, callback=buttonPressed, bouncetime=200)

try:
    initprint()
    dw = DogWalker('Codi',printout,not PI)
    if PI: initButtons()
    while True:
        if not PI:
            ch=ord(msvcrt.getch())
            if ch > 47 and ch < 52:
                dw.processChar(ch-48)
        else:
            time.sleep(20)
except KeyboardInterrupt:
    dw.exit()


