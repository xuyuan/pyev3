#!/usr/bin/env python
'''

http://www.ev3dev.org/docs/tutorials/using-ps3-sixaxis/
http://python-evdev.readthedocs.io/en/latest/
'''

import evdev
import threading

## Some helpers ##

def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.

    val: float or int
    src: tuple
    dst: tuple

    example: print scale(99, (0.0, 99.0), (-1.0, +1.0))
    """
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


def scale_stick(value):
    return scale(value,(0,255),(-100,100))


class Ipega(object):
    def __init__(self, name='ipega Extending Game controller'):
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        fn = None
        for device in devices:
            if device.name == name:
                fn = device.fn
                break
        assert fn
        self.gamepad = evdev.InputDevice(fn)
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        for event in self.gamepad.read_loop():
            print event

if __name__ == '__main__':
    ipega = Ipega()
    import time
    while True:
        time.sleep(0.1)
