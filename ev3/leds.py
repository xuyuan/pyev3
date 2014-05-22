'''
'''


LEDS_PATH = '/sys/class/leds/ev3:'
COLORS = ['green', 'red']
NAMES = ['left', 'right']


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


def set_color(name, color):
    '''turn LED to given color
    parameters
    ----------
        - name: name of LED, e.g. left, right or all
        - color: {'green", 'yellow', 'red'}
    '''
    name_l = name.lower()
    if name_l == 'all':
        for n in NAMES:
            set_color(n, color)
        return

    if name_l not in NAMES:
        raise RuntimeError('unknow LED name: ' + name)

    if color:
        color_l = color.lower()
        if color_l == 'yellow':
            for c in COLORS:
                _set_trigger(c, name, 'default-on')
        elif color_l in COLORS:
            for c in COLORS:
                if c == color_l:
                    _set_trigger(c, name, 'default-on')
                else:
                    _set_trigger(c, name, 'none')
        else:
            raise RuntimeError('unknown color: ' + color)
    else:
        for c in COLORS:
            _set_trigger(c, name, 'none')

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