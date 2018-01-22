#!/usr/bin/env python3
#
#
#
import os
import time
import serial
import re
import Hologram
from Hologram.HologramCloud import HologramCloud
credentials = {'devicekey': 'xyz12345'}

hologram = HologramCloud(credentials, network='cellular')
# cmdres =os.system('gpsctl -n')
global count
def nmea(line):
    global count
    parts = line.split(",")
    if parts[0]=='$GPGGA':
        count = count + 1
        gga(parts)
        if count == 10:
            recv = hologram.sendMessage(line, topics=["MyGps"])
            print(line)
            count = 0



def gga(parts):
    # extract the time
    match = re.match('(\d\d)(\d\d)(\d\d)\.(\d\d\d)',parts[1])
    if match:
        h = match.group(1)
        m = match.group(2)
        s = match.group(3)
        print("Time is %s:%s:%s UTC" % (h,m,s))


ser = serial.Serial('/dev/rfcomm1', timeout=2)
line = ""
count =0
while True:
    ch = ser.read()
    if ch=='\r':
        nmea(line)
        line = ""
        ch = ser.read()   # get the newline
    else:
        line = line + ch
