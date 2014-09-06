# -*- coding: utf-8 -*-
'''Sound module for Lego Mindstorms EV3, includes:
    * Text To Speach
        Please install sox(play) first: apt-get install sox
    * tone
'''

import subprocess
from device import Device

snd_legoev3 = Device('/sys/devices/platform/snd-legoev3')


def beep(hz, t=None):
    '''control the speaker in Tone mode
    @param hz beep at hz Hz, where 0 < hz < 20000. 0 means stopping beeping
    @param beep for t milliseconds, None means beep for ever
    '''
    if t is None or hz == 0:
        snd_legoev3._write('tone', str(hz))
    else:
        cmd = 'beep -f %d -l %d' % (hz, t)
        subprocess.call(cmd.split())


def _say_cmd(text, language):
    return 'espeak "' + text + '" -v ' + language + ' --stdout | play -q -V1 -t wav - echo 0.8 0.8 5 0.7 echo 0.8 0.7 6 0.7 echo 0.8 0.7 10 0.7 gain 10'


def say(text, language='en'):
    subprocess.call(_say_cmd(text, language), shell=True)


def post_say(text, language='en'):
    return subprocess.Popen(_say_cmd(text, language), shell=True)

if __name__ == '__main__':
    say('hi, I am an EV3')
    say('我会说中文', 'zh')

    # twinkle twinkle little star
    beep(262, 180)
    beep(262, 180)
    beep(392, 180)
    beep(392, 180)
    beep(440, 180)
    beep(440, 180)
    beep(392, 380)
    beep(349, 180)
    beep(349, 180)
    beep(330, 180)
    beep(330, 180)
    beep(294, 180)
    beep(294, 180)
    beep(262, 400)

    post_say('good bye')
