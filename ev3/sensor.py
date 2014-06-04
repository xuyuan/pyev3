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

SENSOR_PATH = '/sys/class/msensor/'


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
        return int(self._read('type_id'))

    @property
    def value(self):
        #return [self._read('value' + str(i)) for i in range(self.num_values)]
        self._bin_data_file.seek(0)
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
    sensor_names = os.listdir(SENSOR_PATH)
    return [Sensor(SENSOR_PATH + s) for s in sensor_names]


def find_sensor_path_by_id(type_id):
    '''help function: find sensor path by given type id
    '''
    sensor_names = os.listdir(SENSOR_PATH)
    for s in sensor_names:
        with open(os.path.join(SENSOR_PATH, s + '/type_id'), 'r') as type_id_file:
            type_id_value = int(type_id_file.read())
            if type_id_value == type_id:
                return os.path.join(SENSOR_PATH, s)
    return None


class InfraredSensor(Sensor):
    '''LEGO EV3 Infrared Sensor (45509)
    '''
    def __init__(self, path=None):
        if not path:
            path = find_sensor_path_by_id(33)
        if path:
            super(InfraredSensor, self).__init__(path)
        else:
            raise RuntimeError('No InfraredSensor is connected')


class IRProx(InfraredSensor):
    '''InfraredSensor in IR-PROX mode
    '''
    def __init__(self, path=None):
        super(IRProx, self).__init__(path)
        self.mode = 'IR-PROX'

    @property
    def proximity(self):
        '''[0, 100] in percentage, 0 means very close, and 100 means very far
        '''
        return self.value[0]

    @property
    def distance(self):
        '''distance in meters
        '''
        return self.proximity * 0.7

if __name__ == '__main__':
    all_sensors = all()
    for s in all_sensors:
        print '--------------------'
        print s

    s = IRProx()
    print s
