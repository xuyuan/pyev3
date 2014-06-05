# -*- coding: utf-8 -*-
'''Text To Speach for Lego Mindstorms EV3

Please install sox(play) first: apt-get install sox
'''

import subprocess


def _say_cmd(text, language):
    return 'espeak "' + text + '" -v ' + language + ' --stdout | play -q -V1 -t wav - echo 0.8 0.8 5 0.7 echo 0.8 0.7 6 0.7 echo 0.8 0.7 10 0.7 gain 10'


def say(text, language='en'):
    subprocess.call(_say_cmd(text, language), shell=True)


def post_say(text, language='en'):
    return subprocess.Popen(_say_cmd(text, language), shell=True)


if __name__ == '__main__':
    say('hi, I am an EV3')
    say('我会说中文', 'zh')
    post_say('good bye')
