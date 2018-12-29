import unittest
import collections

from os import path
from shconfparser.reader import Reader
from shconfparser.shsplit import ShowSplit


class TestShowSplit(unittest.TestCase):

    def test_split_data(self):
        file_path = path.abspath('data/shcommands.txt')
        r = Reader(file_path)
        obj = ShowSplit()
        data = obj.split(r.data)
        assert type(data) is collections.OrderedDict
        assert 'running' in data

    def test_split_none_data(self):
        folder_path = path.abspath('data')
        r = Reader(folder_path)
        obj = ShowSplit()
        data = obj.split(r.data)
        assert data is None

    def test_command_not_found(self):
        lst = ['abcd#sh testing', 'testing']
        obj = ShowSplit()
        data = obj.split(lst)
        assert data == {}
        # TODO: need assert log messages
        # assert 'No key found' in 
        
