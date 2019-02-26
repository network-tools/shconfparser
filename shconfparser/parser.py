#!/usr/bin/python

import re, os, logging, json
from collections import OrderedDict
from .shsplit import ShowSplit
from .reader import Reader
from .search import Search


class Parser:
    def __init__(self):
        self.data = OrderedDict()
        self.table = []
        self.header_pattern = r''
        self.header_names = []
        self.column_indexes = []
        self.search = Search()

    def _space_level(self, line):
        return len(line) - len(line.lstrip(' '))

    def _convert_to_dict(self, tree, level=0):
        temp_dict = OrderedDict()
        for i, node in enumerate(tree):
            try:
                next_node = tree[i + 1]
            except IndexError:
                next_node = {'level': -1}

            if node['level'] > level:
                continue
            if node['level'] < level:
                return temp_dict

            if next_node['level'] == level:
                temp_dict[node['key']] = 'None'
            elif next_node['level'] > level:
                temp_dict[node['key']] = self._convert_to_dict(tree[i + 1:], level=next_node['level'])
            else:
                temp_dict[node['key']] = 'None'
                return temp_dict
        return temp_dict

    def _fetch_header(self, lines):
        pattern = re.compile(self.header_pattern)
        for i, line in enumerate(lines):
            result = pattern.match(line)
            if result: return i
        return -1

    def _fetch_column_position(self, header):
        position = []
        for header_name in self.header_names:
            position.append(header.find(header_name))
        return position

    def _fetch_table_column(self, line, start, end, key, data):
        col_data = str(line[start:end]).strip()
        if col_data: data[key] = col_data

    def _fetch_table_row(self, line, data, table):
        if len(line) < self.column_indexes[-1]:
            data[self.header_names[0]] = line.strip()
            return data

        for i, column_index in enumerate(self.column_indexes):
            try:
                start, end = column_index, self.column_indexes[i + 1]
                self._fetch_table_column(line, start, end, self.header_names[i], data)
            except IndexError:
                continue
        self._fetch_table_column(line, start=self.column_indexes[-1], end=len(line), key=self.header_names[-1], data=data)
        table.append(data)
        data = {}
        return data

    def _fetch_table_data(self, lines, header_index, pattern):
        table, data = [], {}
        for i in range(header_index + 1, len(lines)):
            if pattern in lines[i] or len(lines[i]) < 2:
                break
            if '---' in lines[i] or '===' in lines[i]:
                continue
            data = self._fetch_table_row(lines[i], data, table)
        return table

    def _convert(self, lst, re_escape):
        lst1 = []
        for each in lst:
            if re_escape:
                lst1.append(re.escape(each))
            else:
                lst1.append(each.replace(' ', "\s+"))
        return lst1

    def parse_tree(self, lines):
        data = list()
        for i, line in enumerate(lines):
            space = self._space_level(line.rstrip())
            line = line.strip()
            if line != '!' and line != '' and line != 'end':
                data.append({'key': line, 'level': space})
        self.data = self._convert_to_dict(data)
        return self.data

    def parse_data(self, lines):
        self.data = OrderedDict()
        for line in lines:
            line = line.rstrip()
            self.data[line] = 'None'
        return self.data

    def parse_table(self, lines, header_names, pattern='#', re_escape=True):
        self.table_lst = []
        self.header_names = header_names
        self.header_pattern = ' +'.join(self._convert(header_names, re_escape))
        self.header_pattern = '\s*' + self.header_pattern
        header_index = self._fetch_header(lines)
        if header_index == -1:
            logging.error("Couldn't able to find header. validate: {} {}".format(header_names, lines))
            return None
        self.column_indexes = self._fetch_column_position(lines[header_index])
        self.table_lst = self._fetch_table_data(lines, header_index, pattern)
        return self.table_lst

    def split(self, lines, pattern=None):
        self.s = ShowSplit()
        return self.s.split(lines, pattern)

    def read(self, path):
        self.r = Reader(path)
        return self.r.data

    def dump(self, data, indent=None):
        return json.dumps(data, indent=indent)
