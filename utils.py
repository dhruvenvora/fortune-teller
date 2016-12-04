#Utility functions

import datetime as DT

def getTimeString(timestamp):
    tc = 0
    if isinstance(timestamp, str):
        tc = int(timestamp)
    else:
        tc = timestamp
    
    return DT.datetime.fromtimestamp(tc).strftime('%m-%d-%Y %H:%M:%S')

def
