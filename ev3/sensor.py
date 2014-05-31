'''sensors for Lego Mindstorms EV3

https://github.com/mindboards/ev3dev/wiki/Using-Sensors
'''

import os
import array
from device import Device

PY_BIN_DATA_FROMAT = {'u8': 'B',       # usigned char (8-bit)
                      's8': 'b',       # char (8-bit)
                      'u16': 'H',      # usigned short (16-bit)
                      's16': 'h',      # short (16-bit)
                      's16_be': '>h',  # short, big endian (16-bit)
                      's32': 'l',      # int (32-bit)
                      'float': 'f'}    # float (32-bit)


class Sensor(Device):
    def __init__(self, path):
        super(Sensor, self).__init__(path)

        self.modes = {''}
        while '' in self.modes:
            self.modes = self._read('modes').split(' ')
        self._update_num_values()

    def _update_num_values(self):
        self.num_values = int(self._read('num_values'))
        self.bin_data_format = self._read('bin_data_format')
        self._bin_data_formate = PY_BIN_DATA_FROMAT[self.bin_data_format]
        self._bin_data_file = self._open('bin_data', 'r')

    @property
    def type_id(self):
        return self._read('type_id')

    @property
    def value(self):
        #return [self._read('value' + str(i)) for i in range(self.num_values)]
        bin_data = self._bin_data_file.read()
        v = array.array(self._bin_data_formate)
        v.fromstring(bin_data)
        return v[:self.num_values]

    @property
    def mode(self):
        return self._read('mode')

    @mode.setter
    def mode(self, value):
        self._write('mode', value)
        self._update_num_values()

    @property
    def port_name(self):
        return self._read('port_name')

    @property
    def units(self):
        return self._read('units')


def all():
    sensor_path = '/sys/class/msensor/'
    sensor_names = os.listdir(sensor_path)
    return [Sensor(sensor_path + s) for s in sensor_names]


if __name__ == '__main__':
    all_sensors = all()
    for s in all_sensors:
        print '--------------------'
        print s
