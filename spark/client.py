#!/usr/bin/env python

from __future__ import print_function
from socket import socket, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST
from time import sleep
from contextlib import closing

class Rainbow(object):
    STEPS = 0x600
    LEDS = 10
    OFFSET_PER_LED = float(STEPS) / float(LEDS)

    def rgb(self, state):
        substate = state / 256
        progress = state % 256
        result = [0, 0, 0]
        if substate % 2 == 1:
            result[substate / 2] = 255 - progress
        else:
            result[(substate / 2 + 1) % 3] = progress
        result[((substate + 1) % 6) / 2] = 255
        return ''.join(chr(i) for i in result)

    def execute(self, host):
        with closing(socket(type=SOCK_DGRAM)) as s:
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            s.connect((host, 17504))
            while True:
                for i in xrange(0, self.STEPS, 8):
                    s.sendall(''.join(self.rgb(int(round(i + float(j) * self.OFFSET_PER_LED)) % self.STEPS)
                        for j in xrange(self.LEDS)))
                    sleep(0.01)

if __name__ == '__main__':
    from sys import argv, stderr
    try:
        host = argv[1]
    except IndexError:
        print('Usage: {0} <host>'.format(argv[0]), file=stderr)
        raise SystemExit(1)
    else:
        Rainbow().execute(host)
