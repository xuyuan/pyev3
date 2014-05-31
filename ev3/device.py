'''Base class for Sensors and Motors
'''


class Device(object):
    def __init__(self, path):
        self._path = path

    def _open(self, key, mode):
        path = self._path + '/' + key
        return open(path, mode)

    def _read(self, key):
        data = None
        with self._open(key, 'r') as f:
            data = f.read().replace('\n', '')
        return data

    def _write(self, key, value):
        with self._open(key, 'w') as f:
            f.write(value)
            f.flush()

    def __str__(self):
        kv = {}
        for k in dir(self):
            if not k.startswith('_'):
                kv[k] = self.__getattribute__(k)
        return str(kv)
