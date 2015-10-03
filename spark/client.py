#!/usr/bin/env python

from __future__ import print_function
from socket import socket, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST
from time import sleep
from contextlib import closing
from random import shuffle

class Rainbow(object):
    STEPS = 0x600
    LEDS = range(10)
    SKIP = 8

    def offset_per_led(self):
        return float(self.STEPS) / float(len(self.LEDS))

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
                for i in xrange(0, self.STEPS, self.SKIP):
                    s.sendall(''.join(self.rgb(int(round(i + float(j) * self.offset_per_led())) % self.STEPS)
                        for j in self.LEDS))
                    sleep(0.01)

class Fire(Rainbow):
    STEPS = 0x200
    SKIP = 3

    def __init__(self):
        Rainbow.__init__(self)
        shuffle(self.LEDS)

    def rgb(self, state):
        substate = state / 256
        progress = state % 256
        return chr(255) + chr(progress / 3 if substate == 0 else (255 - progress) / 3) + chr(0)

if __name__ == '__main__':
    from sys import argv, stderr
    try:
        host = argv[1]
        effect = globals()[argv[2]]
    except IndexError:
        print('Usage: {0} <host> <effect>'.format(argv[0]), file=stderr)
        raise SystemExit(1)
    except KeyError:
        print('Invalid effect, see source for valid values', file=stderr)
        raise SystemExit(1)
    else:
        effect().execute(host)
