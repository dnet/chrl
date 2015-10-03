from socket import socket, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST
from time import sleep
from contextlib import closing

def rainbow(state):
    substate = state / 256
    progress = state % 256
    result = [0, 0, 0]
    if substate % 2 == 1:
        result[substate / 2] = 255 - progress
    else:
        result[(substate / 2 + 1) % 3] = progress
    result[((substate + 1) % 6) / 2] = 255
    return ''.join(chr(i) for i in result)

STEPS = 0x600
LEDS = 10
OFFSET_PER_LED = float(STEPS) / float(LEDS)

with closing(socket(type=SOCK_DGRAM)) as s:
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    s.connect(('192.168.1.255', 17504))
    while True:
        for i in xrange(0, STEPS, 8):
            s.sendall(''.join(rainbow(int(round(i + float(j) * OFFSET_PER_LED)) % STEPS)
                for j in xrange(LEDS)))
            sleep(0.01)
