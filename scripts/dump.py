#!/usr/bin/env python

import sys
import serial
import MCP2515

s = serial.Serial( sys.argv[1] )

m = MCP2515.MCP2515( s )

m.reset()
m.set_bit_timing( MCP2515.MCP_CBR_16MHz_500kbps_SP75_SJW1 )

m.write_transmit_message( 0, 0x123, map( ord, 'Simon   '  ))
m.write_transmit_message( 1, 0x234, map( ord, 'Foster  ' ))
m.write_transmit_message( 2, 0x345, map( ord, 'Woz Ear ' ))
    
m.set_mode( MCP2515.MCP_NORMAL_MODE )
        
for block in range(8):
    print [ '%02X' % c for c in m.read( 16 * block, count=16 ) ]        