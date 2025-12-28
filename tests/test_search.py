from os import path

import pytest

from shconfparser.parser import Parser


class TestParser:

    @pytest.fixture
    def setup(self):
        file_path = path.abspath("data/shcommands.txt")
        p = Parser()
        file_data = p.read(file_path)
        p.split(file_data)
        p.s.shcmd_dict["running"] = p.parse_tree(p.s.shcmd_dict["running"])
        p.s.shcmd_dict["version"] = p.parse_data(p.s.shcmd_dict["version"])
        header = ["Device ID", "Local Intrfce", "Holdtme", "Capability", "Platform", "Port ID"]
        p.s.shcmd_dict["cdp_neighbors"] = p.parse_table(p.s.shcmd_dict["cdp_neighbors"], header)
        header = ["Interface", "IP-Address", "OK?", "Method", "Status", "Protocol"]
        p.s.shcmd_dict["ip_interface_brief"] = p.parse_table(
            p.s.shcmd_dict["ip_interface_brief"], header
        )
        yield p

    def test_search_in_tree_level(self, setup):
        data = setup.s.shcmd_dict
        pattern = r" privilege level 15"
        m = setup.search.search_in_tree_level(pattern, data["running"], level=10)
        assert pattern.strip() in m

    def test_search_all_in_tree(self, setup):
        data = setup.s.shcmd_dict
        pattern = r"interface\s+FastEthernet.*"
        m = setup.search.search_all_in_tree(pattern, data["running"])
        assert "interface FastEthernet0/0" in m.values()

    def test_search_in_tree(self, setup):
        data = setup.s.shcmd_dict
        pattern = r"Cisco\s+IOS\s+Software.*"
        m = setup.search.search_in_tree(pattern, data["version"])
        assert "Version 12.4(25d)" in m.group(0)

    def test_search_in_table(self, setup):
        data = setup.s.shcmd_dict
        pattern = r"R\d+"
        header = "Device ID"
        m = setup.search.search_in_table(pattern, data["cdp_neighbors"], header)
        assert "Device ID" in m
        assert m["Device ID"] == "R2"

    def test_search_all_in_table(self, setup):
        data = setup.s.shcmd_dict
        pattern = r"FastEthernet.*"
        header = "Interface"
        m = setup.search.search_all_in_table(pattern, data["ip_interface_brief"], header)
        assert type(m) is list
        assert "Interface" in m[0]
        assert m[0]["Interface"] == "FastEthernet0/0"
