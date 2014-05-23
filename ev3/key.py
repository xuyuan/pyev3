'''

https://github.com/mindboards/ev3dev/wiki/Using-the-Buttons
'''

import io
import struct
import threading

KEY_NAME = {103: 'UP',
            108: 'DOWN',
            105: 'LEFT',
            106: 'RIGHT',
            28: 'ENTER',
            1: 'ESC'}

callbacks = []


def connect(func):
    '''register callback to key event
    parameters
    ----------
        - func: func(key, event, time)
    '''
    callbacks.append(func)


def disconnect(func=None):
    '''remove callbacks
    '''
    if func:
        callbacks.remove(func)
    else:
        callbacks.clear()


def main():
    key_file = io.FileIO('/dev/input/by-path/platform-gpio-keys.0-event')
    while True:
        data = key_file.read(16)  # the data is 16 bytes
        seconds = struct.unpack("L", data[0:4])[0]
        microseconds = struct.unpack("L", data[4:8])[0]
        type = struct.unpack("H", data[8:10])[0]
        code = struct.unpack("H", data[10:12])[0]
        value = struct.unpack("I", data[12:16])[0]
        if type:
            key = KEY_NAME[code]
            event = value and 'pressed' or 'released'
            for cb in callbacks:
                cb(key, event, (seconds, microseconds))

thread = threading.Thread(target=main, name='key_loop')
thread.daemon = True
thread.start()


if __name__ == "__main__":
    def print_key(key, event, time):
        print time, key, event
    connect(print_key)
    import time
    while True:
        time.sleep(1)
