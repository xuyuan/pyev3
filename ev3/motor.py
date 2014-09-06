'''motor control for Lego Mindstorms EV3

https://github.com/mindboards/ev3dev/wiki/Using-Motors
'''

import os
from device import Device

MOTOR_PATH = '/sys/bus/legoev3/devices'


class Motor(Device):
    def __init__(self, port):
        path = os.path.join(MOTOR_PATH, 'out' + port + ':motor', 'tacho-motor')
        if not os.path.exists(path):
            raise IOError("no motor is connected to port " + port)
        names = os.listdir(path)
        if len(names) != 1:
            raise IOError("unexpected files in " + path + ':\n' + str(names))
        path = os.path.join(path, names[0])
        super(Motor, self).__init__(path)
        self._position_file = self._open('position', 'w+r')
        self._position_setpoint_file = self._open('position_sp', 'w+r')
        self._speed_file = self._open('pulses_per_second', 'r')
        self._speed_setpoint_file = self._open('pulses_per_second_sp', 'w+r')
        self._power_file = self._open('duty_cycle', 'r')
        self._run_file = self._open('run', 'w+r')

    @property
    def type(self):
        return self._read('type')

    @property
    def position(self):
        '''a read-only indication of how many tacho ticks the driver has counted.
        The number has a range of +/- 2,147,483,648

        remember, the tacho motor counts pulses, not degrees.
        It just happens that the engineers at LEGO designed the motors to count 360 pulses for a full circle!
        '''
        self._position_file.seek(0)
        return int(self._position_file.read())

    @position.setter
    def position(self, v):
        '''useful to clear current value
        '''
        self._position_file.write(str(v))
        self._position_file.flush()

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

        `forever`
        `time`
        `position`
        '''
        return self._read('run_mode')

    @run_mode.setter
    def run_mode(self, v):
        self._write('run_mode', v)

    @property
    def speed_setpoint(self):
        '''
        '''
        return int(self._speed_setpoint_file.read())

    @speed_setpoint.setter
    def speed_setpoint(self, v):
        try:
            nv = min(100, max(-100, int(v)))
            self._speed_setpoint_file.write(str(nv))
            self._speed_setpoint_file.flush()
        except IOError as e:
            raise Exception("I/O error({0}): {1}".format(e.strerror, v))

    @property
    def run(self):
        '''a numerical value - 0 means stop, anthing else means run
        '''
        return int(self._run_file.read())

    @run.setter
    def run(self, v):
        self._run_file.write(str(v))
        self._run_file.flush()

    @property
    def regulation_mode(self):
        '''The regulation_mode attribute has two possible values on and off - the default is off.

        the speed_setpoint in unregulated mode just sends a percentage of the battery voltage to the motor.
        When the batteries get depleted, the percentage stays the same but the resulting voltage at the motor
        goes down in proportion to the battery, and the motor will run slower.

        Turning regulation on in this case will make the EV3 driver the ports a little harder to
        compensate for the lower battery voltage to try and keep the speed at the speed_setpoint.
        '''
        return self._read('regulation_mode')

    @regulation_mode.setter
    def regulation_mode(self, v):
        self._write('regulation_mode', v)

    @property
    def stop_modes(self):
        return self._read('stop_modes').split()

    @property
    def stop_mode(self):
        '''They are `coast` (the default) `brake` and `hold`. In coast mode, when the motor is turned off the internal
        H-bridge that drives the motors is left in a state where there is no load applied to the motor. When you
        set the stop_mode attribute to brake, the H-bridge applies a short across the motor terminals.
        '''
        return self._read('stop_mode')

    @stop_mode.setter
    def stop_mode(self, v):
        self._write('stop_mode', v)

    @property
    def time_setpoint(self):
        '''As soon as we set a value and tell the motor to run,
        it will run for time_setpoint milliseconds from that point in time.
        '''
        return int(self._read('time_sp'))

    @time_setpoint.setter
    def time_setpoint(self, t):
        self._write('time_sp', str(t))

    @property
    def ramp_up(self):
        '''the number of milliseconds that it would take to ramp the motor up from 0% to 100% power.
        '''
        return int(self._read('ramp_up_sp'))

    @ramp_up.setter
    def ramp_up(self, t):
        self._write('ramp_up_sp', str(t))

    @property
    def ramp_down(self):
        '''the number of milliseconds that it would take to ramp the motor down from 100% to 0% power.
        '''
        return int(self._read('ramp_down_sp'))

    @ramp_down.setter
    def ramp_down(self, t):
        self._write('ramp_down_sp', str(t))

    @property
    def position_setpoint(self):
        '''target position when `run_mode` is 'position'
        '''
        return int(self._position_setpoint_file.read())

    @position_setpoint.setter
    def position_setpoint(self, v):
        self._position_setpoint_file.write(str(v))
        self._position_setpoint_file.flush()

    @property
    def position_mode(self):
        ''''absolute' or 'relative' for each target position set by `position_setpoint`.
        The default value for `position_mode` is 'absolute'.
        '''
        return self._read('position_mode')

    @position_mode.setter
    def position_mode(self, v):
        self._write('position_mode', v)

    @property
    def port_name(self):
        return self._read('port_name')


def all():
    motors = []
    for s in ['A', 'B', 'C', 'D']:
        try:
            m = Motor(s)
            motors.append(m)
        except Exception as e:
            print e
    return motors


if __name__ == '__main__':
    #import time
    all_motors = all()
    for m in all_motors:
        print '--------------------'
        print m

    #m = all_motors[0]
    #m.position = 0
    #m.regulation_mode = 'on'
    #m.brake_mode = 'on'
    #m.hold_mode = 'on'
    #m.run_mode = 'position'
    #m.ramp_up = 300
    #m.ramp_down = 300
    #m.speed_setpoint = 50
    #m.position_setpoint = 180
    #m.time_setpoint = 3000
    #m.run = 1
    #m.run = 0
