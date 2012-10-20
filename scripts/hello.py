#!/usr/bin/env python

import sys
import serial
import MCP2515
import time

s = serial.Serial( sys.argv[1] )

mcp = MCP2515.MCP2515( s, debug=0 )

mcp.reset()

mcp.dump()

mcp.set_bit_timing( MCP2515.MCP_CBR_10MHz_500kbps_SP80_SJW1 )

mcp.write_transmit_message( 0, 0x123, map( ord, 'DEADBEEF' ))
mcp.write_transmit_message( 1, 0x234, map( ord, 'CAFEBABE' ))
mcp.write_transmit_message( 2, 0x345, map( ord, 'BAADFOOD' ))
    
mcp.set_mode( MCP2515.MCP_NORMAL_MODE, osm=1 )
        
mcp.dump()

while 1:
    for b in range(3):
        print b

        stat = mcp.RX_status()

        if stat & 0xC0:

            if stat & 0x40:
                # print 'RX0:', [ '%02x' % c for c in mcp.read( 0x60, 16 ) ]
                mcp.bit_modify( MCP2515.MCP_CANINTF, 1, 0 )
        
            if stat & 0x80:
                # print 'RX1:', [ '%02x' % c for c in mcp.read( 0x60, 16 ) ]
                mcp.bit_modify( MCP2515.MCP_CANINTF, 2, 0 )

        mcp.RTS(b)
        time.sleep(0.1)
        mcp.dump()
