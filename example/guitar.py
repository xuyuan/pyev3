'''
'''

import time
from ev3.sensor import IRProx
from ev3.sound import beep


ir = IRProx()

while True:
    d = ir.proximity
    print d
    beep(d * 100, 100)
    #time.sleep(0.2)
