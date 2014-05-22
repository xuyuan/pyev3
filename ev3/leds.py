'''
'''


LEDS_PATH = '/sys/class/leds/ev3:'
COLORS = {'green', 'red'}
NAMES = {'left', 'right'}


def _set_trigger(color, name, trigger):
    '''
    parameters
    ----------
        - color: green or red
        - name: left or right
        - trigger: none, mmc0, timer, heartbeat, default-on
    '''
    led_trigger_path = LEDS_PATH + color + ':' + name + '/trigger'
    with open(led_trigger_path, 'w') as f:
        f.write(trigger)


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

    print 'set left for SD card and right for CPU'
    set_indicator('left', 'sd', 'yellow')
    set_indicator('right', 'cpu', 'red')