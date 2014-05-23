'''
'''

import os


class Sensor(object):
    def __init__(self, path):
        self._path = path
        self.num_values = int(self._read('num_values'))

        self.modes = {''}
        while ''  in self.modes:
            self.modes = set(self._read('modes').split(' '))

    def _read(self, key):
        path = self._path + '/' + key
        data = None
        with open(path, 'r') as f:
            data = f.read().replace('\n', '')
        return data

    @property
    def type_id(self):
        return self._read('type_id')

    @property
    def value(self):
        return [self._read('value' + str(i)) for i in range(self.num_values)]

    @property
    def mode(self):
        return self._read('mode')

def all():
    sensor_path = '/sys/class/msensor/'
    sensor_names = os.listdir(sensor_path)
    return [Sensor(sensor_path + s) for s in sensor_names]


if __name__ == '__main__':
    for s in all():
        print '--------------------'
        print 'type_id:', s.type_id
        print 'modes:', s.modes
        print 'num_values:', s.num_values
        print 'value', s.value
        print 'mode', s.mode
x