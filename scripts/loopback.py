#!/usr/bin/env python

import sys
import serial
import MCP2515
import time

s = serial.Serial( sys.argv[1] )

m = MCP2515.MCP2515( s ) # , debug=1 )

m.reset()

m.dump()

m.set_bit_timing( MCP2515.MCP_CBR_16MHz_500kbps_SP75_SJW1 )

m.write_transmit_message( 0, 0x123, map( ord, 'DEADBEEF' ))
m.write_transmit_message( 1, 0x234, map( ord, 'CAFEBABE' ))
m.write_transmit_message( 2, 0x345, map( ord, 'BAADFOOD' ))
    
m.set_mode( MCP2515.MCP_LOOPBACK_MODE )
        
m.dump()

while 1:
    for b in range(3):

        m.RTS(b)

        stat = m.RX_status()

        if stat & 0xC0:

            if stat & 0x40:
                print 'RX0:', [ '%02x' % c for c in m.read( 0x60, 16 ) ]
                m.bit_modify( MCP2515.MCP_CANINTF, 1, 0 )
        
            if stat & 0x80:
                print 'RX1:', [ '%02x' % c for c in m.read( 0x60, 16 ) ]
                m.bit_modify( MCP2515.MCP_CANINTF, 2, 0 )
        else:    
           print '.', 
           continue 

        time.sleep(1)
