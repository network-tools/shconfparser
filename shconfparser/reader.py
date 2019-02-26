from os import path
from io import open


class Reader:
    def __init__(self, path):
        self.path = path
        self.data = self.read()

    def _isfile(self):
        if path.exists(self.path):
            return path.isfile(self.path)

    def read(self):
        if self._isfile():
            with open(self.path) as f:
                return f.readlines()
