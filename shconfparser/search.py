from collections import OrderedDict
import re


class Search:
    def __init__(self):
        pass

    def search_in_tree(self, pattern, data=None):
        if data == None: return None
        pattern = re.compile(pattern)
        for key in data.keys():
            if pattern.match(key): return pattern.match(key)

    def search_all_in_tree(self, pattern, data=None):
        if data == None: return None
        pattern = re.compile(pattern)
        match = OrderedDict()
        for key in data.keys():
            if pattern.match(key):
                match[pattern.match(key)] = key
        return match if len(match) else None

    def search_in_table(self, pattern, data=None, header_column=None):
        if data == None: return None
        pattern = re.compile(pattern)
        for each_row in data:
            if pattern.match(each_row[header_column]): return each_row

    def search_all_in_table(self, pattern, data=None, header_column=None):
        if data == None: return None
        pattern = re.compile(pattern)
        match = []
        for each_row in data:
            if pattern.match(each_row[header_column]):
                match.append(each_row)
        return match if len(match) else None
