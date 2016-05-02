'''use motors to make robot move around
'''

from motor import Motor
from math import degrees


class MoveTank(object):
    '''move base for differential-drive robot
    '''
    def __init__(self, wheel_radius=0.016, base_width=0.18, left_motor_port='B', right_motor_port='C'):
        self.left_motor = Motor(left_motor_port)
        self.right_motor = Motor(right_motor_port)
        self.base_width = base_width
        self.wheel_radius = wheel_radius
        self._twist = [0, 0]

    @property
    def twist(self):
        return self._twist

    @twist.setter
    def twist(self, v):
        if v[0] == 0 and v[1] == 0:
            self.stop()
        else:
            rot = v[1] * self.base_width / 2
            lv = v[0] + rot
            rv = v[0] - rot
            self.left_motor.speed_setpoint = int(lv / self.wheel_radius)
            self.right_motor.speed_setpoint = int(rv / self.wheel_radius)
            self.left_motor.command = 'run-forever'
            self.right_motor.command = 'run-forever'
        self._twist = v

    def move(self, d):
        ang = int(degrees(d / self.wheel_radius))
        self.left_motor.position_setpoint = ang
        self.right_motor.position_setpoint = ang
        self.left_motor.command = 'run-to-rel-pos'
        self.right_motor.command = 'run-to-rel-pos'

    def stop(self):
        self.left_motor.command = 'stop'
        self.right_motor.command = 'stop'

if __name__ == '__main__':
    import time
    move = MoveTank()
    #move.twist = [1, 0]
    #time.sleep(5)
    #move.stop()
    move.move(0.05)
