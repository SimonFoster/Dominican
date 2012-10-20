#!/usr/bin/env python

import serial
import time

# s = serial.Serial( 'com19' )		# Windows eg.
s = serial.Serial( '/dev/ttyACM0' )	# Linux eg.

while 1:
    for i in [ 0x20, 0x40, 0x00, 0x60 ]:
        print hex(i)
        s.write( chr(i) )
        time.sleep( 1 )
