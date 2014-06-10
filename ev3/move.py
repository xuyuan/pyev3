'''use motors to make robot move around
'''

from motor import Motor


class MoveTank(object):
    '''move base for differential-drive robot
    '''
    def __init__(self, base_width, left_motor_port='B', right_motor_port='C'):
        self.left_motor = Motor(left_motor_port)
        self.right_motor = Motor(right_motor_port)
        self.base_width = base_width
        self._twist = [0, 0]

    @property
    def twist(self):
        return self._twist

    @twist.setter
    def twist(self, v):
        if v[0] == 0 and v[1] == 0:
            self.stop()
        else:
            rot = v[1]
            lv = rot
            rv = -rot
            if abs(rot) < 100:
                lv += v[0]
                rv += v[0]
            self.left_motor.run_mode = 'forever'
            self.right_motor.run_mode = 'forever'
            self.left_motor.speed_setpoint = lv
            self.right_motor.speed_setpoint = rv
            self.left_motor.run = 1
            self.right_motor.run = 1
        self._twist = v

    def stop(self):
        self.left_motor.run = 0
        self.right_motor.run = 0
