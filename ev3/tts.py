# -*- coding: utf-8 -*-
'''Text To Speach for Lego Mindstorms EV3
'''

import subprocess


def say(text, language='en'):
    subprocess.call('espeak "' + text + '" -v ' + language + ' --stdout | play -q -V1 -t wav - echo 0.8 0.8 5 0.7 echo 0.8 0.7 6 0.7 echo 0.8 0.7 10 0.7', shell=True)


if __name__ == '__main__':
    say('hi, I am an EV3')
    say('我会说中文', 'zh')
