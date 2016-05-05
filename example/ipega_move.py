#!/usr/bin/env python
'''
'''

from ev3.ipega import Ipega
from ev3.move import MoveTank
import evdev


class IpegaTank(Ipega):
    def __init__(self):
        super(IpegaTank, self).__init__()
        self.move = MoveTank()
        self.twist = [0, 0]

    def run(self):
        for event in self.gamepad.read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == 5:  # ABS_Z
                    self.twist[0] = -(event.value / 255.0 * 2 - 1) * 0.05
                if event.code == 0:  # ABS_Y
                    self.twist[1] = -(event.value / 255.0 * 2 - 1) * 0.3
                self.move.twist = self.twist

if __name__ == '__main__':
    ipega_tank = IpegaTank()
    try:
        ipega_tank.run()
    finally:
        ipega_tank.move.stop()
