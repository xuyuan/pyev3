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
        else:
            head_motor.run_mode = 'forever'
            if head_motor.position > 90:
                head_scan_direction = -1
            elif head_motor.position < -90:
                head_scan_direction = 1
            head_motor.speed_setpoint = head_scan_direction * 15
            scanning = True

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
