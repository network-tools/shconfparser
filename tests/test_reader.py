import unittest

from os import path
from shconfparser.reader import Reader


class TestReader(unittest.TestCase):

    def test_given_file_path(self):
        file_path = path.abspath('data/shrun.txt')
        obj = Reader(file_path)
        assert type(obj.data) is list

    def test_given_folder_path(self):
        folder_path = path.abspath('data')
        obj = Reader(folder_path)
        assert obj.data is None
