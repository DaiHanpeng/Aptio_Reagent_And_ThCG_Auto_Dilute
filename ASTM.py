__author__ = 'Z003CA1K'

IDLE_STATUS         = 0
SENDING_STATUS      = 1
RECEIVING_STATUS    = 2
"""
ASTM_STX    = 0x02
ASTM_ETX    = 0x03
ASTM_EOT    = 0x04
ASTM_ENQ    = 0x05
ASTM_ACK    = 0x06
ASTM_CR	    = 0x0d
ASTM_LF	    = 0x0a
ASTM_NAK    = 0x15
ASTM_ETB    = 0x17

"""

#: Message start token.
ASTM_STX = b'\x02'
#: Message end token.
ASTM_ETX = b'\x03'
#: ASTM session termination token.
ASTM_EOT = b'\x04'
#: ASTM session initialization token.
ASTM_ENQ = b'\x05'
#: Command accepted token.
ASTM_ACK = b'\x06'
#: Command rejected token.
ASTM_NAK = b'\x15'
#: Message chunk end token.
ASTM_ETB = b'\x17'
ASTM_LF  = b'\x0A'
ASTM_CR  = b'\x0D'

ASTM_ACTION_NEW     = 1
ASTM_ACTION_ADD     = 2
ASTM_ACTION_CANCEL  = 3





