#!/usr/bin/python
import time
from messages import message

def initprint():
    pass

    
def printout(string, sleep=None, *args):
    print(message(string,*args))
    if sleep != None:
        time.sleep(sleep)

