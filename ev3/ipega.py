#!/usr/bin/env python
'''

http://www.ev3dev.org/docs/tutorials/using-ps3-sixaxis/
http://python-evdev.readthedocs.io/en/latest/
'''

import evdev


class Ipega(object):
    def __init__(self, name='ipega Extending Game controller'):
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        fn = None
        for device in devices:
            if device.name == name:
                fn = device.fn
                break
        if fn is None:
            raise RuntimeError("can't find device: " + name)
        self.gamepad = evdev.InputDevice(fn)

    def run(self):
        for event in self.gamepad.read_loop():
            print event, (evdev.categorize(event))

if __name__ == '__main__':
    ipega = Ipega()
    ipega.run()
