# Generated by h2py from mcp2515_defs.h
MCP_SIDH = 0
MCP_SIDL = 1
MCP_EID8 = 2
MCP_EID0 = 3
MCP_TXB_EXIDE_M = 0x08
MCP_DLC_MASK = 0x0F
MCP_RTR_MASK = 0x40
MCP_RXB_RX_ANY = 0x60
MCP_RXB_RX_EXT = 0x40
MCP_RXB_RX_STD = 0x20
MCP_RXB_RX_STDEXT = 0x00
MCP_RXB_RX_MASK = 0x60
MCP_RXB_BUKT_MASK = (1<<2)
MCP_TXB_TXBUFE_M = 0x80
MCP_TXB_ABTF_M = 0x40
MCP_TXB_MLOA_M = 0x20
MCP_TXB_TXERR_M = 0x10
MCP_TXB_TXREQ_M = 0x08
MCP_TXB_TXIE_M = 0x04
MCP_TXB_TXP10_M = 0x03
MCP_TXB_RTR_M = 0x40
MCP_RXB_IDE_M = 0x08
MCP_RXB_RTR_M = 0x40
MCP_STAT_RXIF_MASK = (0x03)
MCP_STAT_RX0IF = (1<<0)
MCP_STAT_RX1IF = (1<<1)
MCP_EFLG_RX1OVR = (1<<7)
MCP_EFLG_RX0OVR = (1<<6)
MCP_EFLG_TXBO = (1<<5)
MCP_EFLG_TXEP = (1<<4)
MCP_EFLG_RXEP = (1<<3)
MCP_EFLG_TXWAR = (1<<2)
MCP_EFLG_RXWAR = (1<<1)
MCP_EFLG_EWARN = (1<<0)
MCP_EFLG_ERRORMASK = (0xF8)
MCP_RXF0SIDH = 0x00
MCP_RXF0SIDL = 0x01
MCP_RXF0EID8 = 0x02
MCP_RXF0EID0 = 0x03
MCP_RXF1SIDH = 0x04
MCP_RXF1SIDL = 0x05
MCP_RXF1EID8 = 0x06
MCP_RXF1EID0 = 0x07
MCP_RXF2SIDH = 0x08
MCP_RXF2SIDL = 0x09
MCP_RXF2EID8 = 0x0A
MCP_RXF2EID0 = 0x0B
MCP_CANSTAT = 0x0E
MCP_CANCTRL = 0x0F
MCP_RXF3SIDH = 0x10
MCP_RXF3SIDL = 0x11
MCP_RXF3EID8 = 0x12
MCP_RXF3EID0 = 0x13
MCP_RXF4SIDH = 0x14
MCP_RXF4SIDL = 0x15
MCP_RXF4EID8 = 0x16
MCP_RXF4EID0 = 0x17
MCP_RXF5SIDH = 0x18
MCP_RXF5SIDL = 0x19
MCP_RXF5EID8 = 0x1A
MCP_RXF5EID0 = 0x1B
MCP_TEC = 0x1C
MCP_REC = 0x1D
MCP_RXM0SIDH = 0x20
MCP_RXM0SIDL = 0x21
MCP_RXM0EID8 = 0x22
MCP_RXM0EID0 = 0x23
MCP_RXM1SIDH = 0x24
MCP_RXM1SIDL = 0x25
MCP_RXM1EID8 = 0x26
MCP_RXM1EID0 = 0x27
MCP_CNF3 = 0x28
MCP_CNF2 = 0x29
MCP_CNF1 = 0x2A
MCP_CANINTE = 0x2B
MCP_CANINTF = 0x2C
MCP_EFLG = 0x2D
MCP_TXB0CTRL = 0x30
MCP_TXB1CTRL = 0x40
MCP_TXB2CTRL = 0x50
MCP_RXB0CTRL = 0x60
MCP_RXB0SIDH = 0x61
MCP_RXB1CTRL = 0x70
MCP_RXB1SIDH = 0x71
MCP_TX_INT = 0x1C
MCP_TX01_INT = 0x0C
MCP_RX_INT = 0x03
MCP_NO_INT = 0x00
MCP_TX01_MASK = 0x14
MCP_TX_MASK = 0x54
MCP_WRITE = 0x02
MCP_READ = 0x03
MCP_BITMOD = 0x05
MCP_LOAD_TX0 = 0x40
MCP_LOAD_TX1 = 0x42
MCP_LOAD_TX2 = 0x44
MCP_RTS_TX0 = 0x81
MCP_RTS_TX1 = 0x82
MCP_RTS_TX2 = 0x84
MCP_RTS_ALL = 0x87
MCP_READ_RX0 = 0x90
MCP_READ_RX1 = 0x94
MCP_READ_STATUS = 0xA0
MCP_RX_STATUS = 0xB0
MCP_RESET = 0xC0
MODE_NORMAL = 0x00
MODE_SLEEP = 0x20
MODE_LOOPBACK = 0x40
MODE_LISTENONLY = 0x60
MODE_CONFIG = 0x80
MODE_POWERUP = 0xE0
MODE_MASK = 0xE0
ABORT_TX = 0x10
MODE_ONESHOT = 0x08
CLKOUT_ENABLE = 0x04
CLKOUT_DISABLE = 0x00
CLKOUT_PS1 = 0x00
CLKOUT_PS2 = 0x01
CLKOUT_PS4 = 0x02
CLKOUT_PS8 = 0x03
SJW1 = 0x00
SJW2 = 0x40
SJW3 = 0x80
SJW4 = 0xC0
BTLMODE = 0x80
SAMPLE_1X = 0x00
SAMPLE_3X = 0x40
SOF_ENABLE = 0x80
SOF_DISABLE = 0x00
WAKFIL_ENABLE = 0x40
WAKFIL_DISABLE = 0x00
MCP_RX0IF = 0x01
MCP_RX1IF = 0x02
MCP_TX0IF = 0x04
MCP_TX1IF = 0x08
MCP_TX2IF = 0x10
MCP_ERRIF = 0x20
MCP_WAKIF = 0x40
MCP_MERRF = 0x80
