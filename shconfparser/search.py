"""
Goal: To search the given text in the data of type dict
"""

from collections import OrderedDict
import re


class Search:
    def __init__(self):
        pass

    def validate(self, data, dtype=OrderedDict):
        """
        This method validates the given data
        """
        if data == None:
            return None
        if type(data) != dtype:
            return None
        return True

    def get_pattern(self, pattern, strip=True):
        """
        This method converts the given string to regex pattern
        """
        try:
            if type(pattern) == re.Pattern:
                return pattern
        except AttributeError:
            if type(pattern) != str:
                return pattern

        if strip and type(pattern) == str:
            pattern = pattern.strip()

        return re.compile(pattern)

    def search_in_tree(self, pattern, data=None):
        if not self.validate(data):
            return None

        p = self.get_pattern(pattern)
        for key in data.keys():
            res = p.match(key)
            if res:
                return res
        return None

    def search_all_in_tree(self, pattern, data=None):
        if not self.validate(data):
            return None

        p = self.get_pattern(pattern)
        match = OrderedDict()
        for key in data.keys():
            res = p.match(key)
            if res:
                match[res] = key
        return match if len(match) else None

    def search_in_tree_level(self, pattern, data=None, level=0):
        if not self.validate(data):
            return None

        p = self.get_pattern(pattern)
        for key in data:
            if p.match(key):
                return key
            if data[key] == None:
                continue
            if type(data[key]) == OrderedDict and level > 0:
                res = self.search_in_tree_level(p, data[key], level=level - 1)
                if res:
                    return res
        return None

    def search_in_table(self, pattern, data=None, header_column=None):
        if not self.validate(data, dtype=list):
            return None

        p = self.get_pattern(pattern)
        for each_row in data:
            if p.match(each_row[header_column]):
                return each_row

    def search_all_in_table(self, pattern, data=None, header_column=None):
        if not self.validate(data, dtype=list):
            return None

        p = self.get_pattern(pattern)
        match = []
        match = []
        for each_row in data:
            if p.match(each_row[header_column]):
                match.append(each_row)
        return match if len(match) else None
