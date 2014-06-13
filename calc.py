#!/usr/bin/env python

from __future__ import division

current = 0.020 # A
forward_voltage = {'R': 1.9, 'G': 3.3, 'B': 3.3} # V
input_voltage = 5 # V

for color, fw in sorted(forward_voltage.iteritems(), reverse=True):
    print '{0} = {1} Ohms'.format(color, (input_voltage - fw) / current)
