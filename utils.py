#Utility functions

import datetime as DT
#import time


def getTimeString(timestamp):
    tc = 0
    if isinstance(timestamp, str):
        tc = int(timestamp)
    else:
        tc = timestamp
    #return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(1480719600))
    # Get UTC Time
    tc += 28800 # 28800 is 8 hours. This is done to get UTC
    return DT.datetime.fromtimestamp(tc).strftime('%m-%d-%Y %H:%M:%S')

