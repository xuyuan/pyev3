# -*- coding: utf-8 -*-
'''Text To Speach for Lego Mindstorms EV3
'''

import subprocess


def say(text, language='en'):
    subprocess.call('espeak "' + text + '" -v ' + language + ' -p 20 --stdout | aplay -q', shell=True)


if __name__ == '__main__':
    say('hi, I am an EV3')
    say('我会说中文', 'zh')
