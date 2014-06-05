'''use IR sensor as head to focus on beacon
'''

import time
from sensor import IRSeeker
from motor import Motor

ir = IRSeeker()
motor = Motor('A')
motor.brake_mode = 'off'
motor.regulation_mode = 'on'
motor.run_mode = 'position'
motor.position_mode = 'relative'
motor.ramp_up = 300
motor.ramp_down = 300
motor.speed_setpoint = 20


try:
    while True:
        heading, distance = ir.heading_and_distance
        if distance > 0:
            #print heading, distance
            motor.position_setpoint = int(heading * 0.3)
            motor.run = 1
        time.sleep(0.1)
finally:
    motor.run = 0
