'''use IR sensor as head to focus on beacon
'''

import time
from sensor import IRSeeker
from motor import Motor
import leds
import tts

ir = IRSeeker()
head_motor = Motor('A')
head_motor.position = 0
head_motor.brake_mode = 'off'
head_motor.regulation_mode = 'on'
head_motor.ramp_up = 300
head_motor.ramp_down = 300
head_motor.speed_setpoint = 20


left_motor = Motor('B')
right_motor = Motor('C')

for m in [left_motor, right_motor]:
    m.ramp_up = 300
    m.ramp_down = 300
    m.speed_setpoint = 20

head_scan_direction = 1
scanning = False
state_changed = False

try:
    while True:
        heading, distance = ir.heading_and_distance
        last_scanning = scanning
        if distance > 0:
            head_motor.run_mode = 'forever'
            head_motor.speed_setpoint = heading
            scanning = False

            rot = heading + head_motor.position
            forward = (distance - 0.5) * 200
            left_motor.run_mode = 'forever'
            left_motor.speed_setpoint = rot + forward
            right_motor.run_mode = 'forever'
            right_motor.speed_setpoint = -rot + forward
            left_motor.run = 1
            right_motor.run = 1
        else:
            head_motor.run_mode = 'forever'
            if head_motor.position > 145:
                head_scan_direction = -1
            elif head_motor.position < -145:
                head_scan_direction = 1
            head_motor.speed_setpoint = head_scan_direction * 15
            scanning = True
            left_motor.run = 0
            right_motor.run = 0

        head_motor.run = 1
        if scanning != last_scanning:
            leds.set_color('all', 'green' if scanning else 'red')
            if not scanning:
                tts.post_say('I see you!')
            else:
                tts.post_say('where are you?')
        time.sleep(0.1)
finally:
    head_motor.run_mode = 'position'
    head_motor.position_mode = 'absolute'
    head_motor.position_setpoint = 0
    head_motor.run = 1
    left_motor.run = 0
    right_motor.run = 0