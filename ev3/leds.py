'''LED control for Lego Mindstorms EV3
'''


LEDS_PATH = '/sys/class/leds/ev3:'
COLORS = {'green', 'red'}
NAMES = {'left', 'right'}

TRIGGERS = {}
for c in COLORS:
    for n in NAMES:
        path = LEDS_PATH + n + ':' + c + ':ev3dev/trigger'
        TRIGGERS[c + n] = open(path, 'wb')


def _set(color, name, key, value):
    led_key_path = LEDS_PATH + name + ':' + color + ':ev3dev/' + key
    with open(led_key_path, 'w') as f:
        f.write(value)
        f.flush()


def _set_trigger(color, name, trigger):
    '''
    parameters
    ----------
        - color: green or red
        - name: left or right
        - trigger: none, mmc0, timer, heartbeat, default-on
    '''
    f = TRIGGERS[color + name]
    f.write(trigger)
    f.flush()


def _set_trigger_ext(color, name, trigger):
    if name not in NAMES:
        raise RuntimeError('unknow LED name: ' + name)

    if color:
        if color == 'yellow':
            for c in COLORS:
                _set_trigger(c, name, trigger)
        elif color in COLORS:
            for c in COLORS:
                if c == color:
                    _set_trigger(c, name, trigger)
                else:
                    _set_trigger(c, name, 'none')
        else:
            raise RuntimeError('unknown color: ' + color)
    else:
        for c in COLORS:
            _set_trigger(c, name, 'none')


def set_color(name, color):
    '''turn LED to given color
    parameters
    ----------
        - name: name of LED, e.g. {'left', 'right', 'all'}
        - color: {'green', 'yellow', 'red'}
    '''
    if name == 'all':
        for n in NAMES:
            set_color(n, color)
        return

    _set_trigger_ext(color, name, 'default-on')


def set_indicator(name, indicator, color):
    '''makes the LED blink when there is activity from indicator
    parameters
    ----------
        - name: name of LED, e.g. {'left', 'right', 'all'}
        - indicator: {'sd', 'cpu'}
    '''
    if name == 'all':
        for n in NAMES:
            set_indicator(n, indicator)
        return

    if name not in NAMES:
        raise RuntimeError('unknow LED name: ' + name)

    if indicator == 'sd':
        _set_trigger_ext(color, name, 'mmc0')
    elif indicator == 'cpu':
        _set_trigger_ext(color, name, 'heartbeat')
    else:
        raise RuntimeError('unknow indicator name: ' + indicator)


def set_blink(name, color, time_on=500, time_off=500):
    '''make the LED blink
    parameters
    ----------
        - name: name of LED, e.g. {'left', 'right', 'all'}
        - color: {'green', 'yellow', 'red'}
        - time_on: time in milliseconds when LED is on
        - time_off: time in milliseconds when LED is off
    '''
    if name == 'all':
        for n in NAMES:
            set_blink(n, color, time_on, time_off)
        return

    _set_trigger_ext(color, name, 'timer')
    if color == 'yellow':
        for c in COLORS:
            _set(c, name, 'delay_on', str(time_on))
            _set(c, name, 'delay_off', str(time_off))
    elif color in COLORS:
        _set(color, name, 'delay_on', str(time_on))
        _set(color, name, 'delay_off', str(time_off))
    else:
        raise RuntimeError('unknown color: ' + color)


if __name__ == '__main__':
    from time import sleep
    print 'set_color all None'
    set_color('all', None)
    sleep(1)

    print 'set_color left green'
    set_color('left', 'green')
    sleep(1)

    print 'set_color left None'
    set_color('left', None)
    sleep(1)

    print 'set_color right red'
    set_color('right', 'red')
    sleep(1)

    print 'set_color right yellow'
    set_color('right', 'yellow')
    sleep(1)

    print 'set_color all green'
    set_color('all', 'green')
    sleep(1)

    print 'set_blink all red'
    set_blink('all', 'red', time_on=700, time_off=300)
    sleep(10)

    print 'set left for SD card and right for CPU'
    set_indicator('left', 'sd', 'yellow')
    set_indicator('right', 'cpu', 'red')
