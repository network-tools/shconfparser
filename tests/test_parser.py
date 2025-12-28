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
        yield p

    def test_data_parser(self, setup):
        data = setup.s.shcmd_dict
        assert "version" in data
        result = setup.parse_data(data["version"])
        assert result != {}
        assert "R1 uptime is 10 minutes" in result

    def test_tree_parser(self, setup):
        data = setup.s.shcmd_dict
        assert "running" in data
        result = setup.parse_tree(data["running"])
        assert result != {}
        assert "line vty 0 4" in result

    def test_table_parser(self, setup):
        data = setup.s.shcmd_dict
        assert "cdp_neighbors" in data
        header = ["Device ID", "Local Intrfce", "Holdtme", "Capability", "Platform", "Port ID"]
        result = setup.parse_table(data["cdp_neighbors"], header)
        assert result != []
        assert type(result[0]) is dict
        assert "Device ID" in result[0]
        assert result[0]["Device ID"] == "R2"

    def test_table_parser_multiple_line(self, setup):
        data = {
            "cdp_neighbors": [
                "R1#show cdp neighbors",
                "Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge",
                "S - Switch, H - Host, I - IGMP, r - Repeater",
                "",
                "Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID",
                "ajskdjfajfajlsfjabcdefgh",
                "                 Fas 0/0            164        R S I      3725      Fas 0/0",
                "R1#",
            ]
        }
        assert "cdp_neighbors" in data
        header = ["Device ID", "Local Intrfce", "Holdtme", "Capability", "Platform", "Port ID"]
        result = setup.parse_table(data["cdp_neighbors"], header)
        assert result != []
        assert type(result[0]) is dict
        assert "Device ID" in result[0]
        assert result[0]["Platform"] == "3725"

    def test_table_parser_header_mismatch(self, setup):
        data = setup.s.shcmd_dict
        assert "cdp_neighbors" in data
        header = [" Device ID", "Local Intrfce", "Holdtme", "Capability", "Platform", "Port ID"]
        result = setup.parse_table(data["cdp_neighbors"], header)
        assert result is None
        # TODO: need to check log message

    def test_dump(self, setup):
        data = setup.s.shcmd_dict
        assert type(setup.dump(data)) is str
