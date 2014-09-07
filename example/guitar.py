'''
'''

import time
from ev3.sensor import IRProx, TouchSensor
from ev3.sound import beep


ir = IRProx()
tc = TouchSensor()

# C note from http://liutaiomottola.com/formulae/freqtab.htm
note_frequency = [16, 33, 65, 130, 262, 523, 1047, 2093, 4186, 8372]

while True:
    d = ir.proximity
    d = d / 9 + 1  # about 1 ~ 7
    d = min(7, d)
    f = note_frequency[d]
    #print f
    if tc.released:
        beep(f)
    else:
        beep(0)
    time.sleep(0.01)
