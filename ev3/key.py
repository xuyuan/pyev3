'''

https://github.com/mindboards/ev3dev/wiki/Using-the-Buttons
'''

import io
import struct


KEY_NAME = {103: 'UP',
            108: 'DOWN',
            105: 'LEFT',
            106: 'RIGHT',
            28: 'ENTER',
            1: 'ESC'}


def test_bit(bit, bytes):
    # bit in bytes is 1 when released and 0 when pressed
    return not bool(bytes[bit / 8] & 1 << bit % 8)

if __name__ == "__main__":
    key_file = io.FileIO('/dev/input/by-path/platform-gpio-keys.0-event')
    while True:
        data = key_file.read(16)  # the data is 16 bytes
        secconds = struct.unpack("L", data[0:4])[0]
        microseconds = struct.unpack("L", data[4:8])[0]
        type = struct.unpack("H", data[8:10])[0]
        code = struct.unpack("H", data[10:12])[0]
        value = struct.unpack("I", data[12:16])[0]
        if type:
            print secconds, microseconds, type, KEY_NAME[code], value
