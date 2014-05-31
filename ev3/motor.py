'''motor control for Lego Mindstorms EV3

https://github.com/mindboards/ev3dev/wiki/Using-Motors
'''

import os
from device import Device


class Motor(Device):
    def __init__(self, path):
        super(Motor, self).__init__(path)
        self._position_file = self._open('position', 'r')
        self._speed_file = self._open('speed', 'r')
        self._speed_setpoint_file = self._open('speed_setpoint', 'w+r')
        self._power_file = self._open('power', 'r')
        self._run_file = self._open('run', 'w+r')

    @property
    def type(self):
        return self._read('type')

    @property
    def position(self):
        '''a read-only indication of how many tacho ticks the driver has counted.
        The number has a range of +/- 2,147,483,648
        '''
        return int(self._position_file.read())

    @property
    def speed(self):
        '''a read-only indication of how fast the motor is turning.
        It's not measured in any particular units. The speed ranges in value from -100 to +100,
        where 100 is the maximum practical speed of the motor when it is driven at 100% power
        on an EV3 with fresh batteries. In most cases, you will never see a speed near 100%.

        You can read the motor speed at any time, even if the motor is being rotated by hand!

        Positive speeds correspond to increasing position counts,
        negative speeds correspond to decreasing position counts.
        '''
        return int(self._speed_file.read())

    @property
    def power(self):
        ''' a read-only indication of how hard the motor is being driven.
        It's measured in duty-cycle percentage. That's just fancy terminology for the percentage
        of the battery voltage being used to drive the motor.
        The power ranges in value from -100 to +100, where 100% is driving the motor as hard as
        posible in the positive direction, and -100 driving the motor hard in the negative direction.

        Positive speeds correspond to increasing position counts,
        negative speeds correspond to decreasing position counts.
        '''
        return int(self._power_file.read())

    @property
    def state(self):
        '''a read-only indication of what state the motor is in.
        Depending on what you're doing, you'll get different results when reading this attribute.
        The result is a descriptive text string that represents the state of the motor driver.
        '''
        return self._read('state')

    @property
    def run_mode(self):
        '''It determines how the motor is going to run.
        The default `run_mode` when you plug in a motor is `forever`.
        '''
        return self._read('run_mode')

    @property
    def speed_setpoint(self):
        '''
        '''
        return int(self._speed_setpoint_file.read())

    @speed_setpoint.setter
    def speed_setpoint(self, v):
        self._speed_setpoint_file.write(str(v))
        self._speed_setpoint_file.flush()

    @property
    def run(self):
        '''a numerical value - 0 means stop, anthing else means run
        '''
        return int(self._run_file.read())

    @run.setter
    def run(self, v):
        self._run_file.write(str(v))
        self._run_file.flush()


def all():
    motor_path = '/sys/class/tacho-motor/'
    sensor_names = os.listdir(motor_path)
    return [Motor(motor_path + s) for s in sensor_names]


if __name__ == '__main__':
    import time
    all_motors = all()
    for m in all_motors:
        print '--------------------'
        print m

    m = all_motors[0]
    m.speed_setpoint = 50
    m.run = 1
    time.sleep(3)
    m.speed_setpoint = 100
    time.sleep(3)
    m.run = 0
