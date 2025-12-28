"""Tests for XPath query functionality."""

from collections import OrderedDict

import pytest

from shconfparser.exceptions import SearchError
from shconfparser.parser import Parser
from shconfparser.xpath import XPath


@pytest.fixture
def sample_tree():
    """Create a sample configuration tree for testing."""
    tree = OrderedDict(
        [
            (
                "interface",
                OrderedDict(
                    [
                        (
                            "GigabitEthernet0-0-1",
                            OrderedDict(
                                [
                                    ("description", "WAN Interface"),
                                    (
                                        "ip",
                                        OrderedDict(
                                            [
                                                ("address", "192.168.1.1 255.255.255.0"),
                                                ("nat", "outside"),
                                            ]
                                        ),
                                    ),
                                    ("shutdown", ""),
                                ]
                            ),
                        ),
                        (
                            "GigabitEthernet0-0-2",
                            OrderedDict(
                                [
                                    ("description", "LAN Interface"),
                                    (
                                        "ip",
                                        OrderedDict(
                                            [
                                                ("address", "10.0.0.1 255.255.255.0"),
                                                ("nat", "inside"),
                                            ]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                        (
                            "Loopback0",
                            OrderedDict(
                                [
                                    ("description", "Loopback"),
                                    (
                                        "ip",
                                        OrderedDict(
                                            [
                                                ("address", "1.1.1.1 255.255.255.255"),
                                            ]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            ("hostname", "Router1"),
            (
                "router",
                OrderedDict(
                    [
                        (
                            "bgp",
                            OrderedDict(
                                [
                                    (
                                        "65000",
                                        OrderedDict(
                                            [
                                                (
                                                    "neighbor",
                                                    OrderedDict(
                                                        [
                                                            (
                                                                "10.0.0.2",
                                                                OrderedDict(
                                                                    [
                                                                        ("remote-as", "65001"),
                                                                    ]
                                                                ),
                                                            ),
                                                        ]
                                                    ),
                                                ),
                                            ]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        ]
    )
    return tree


class TestXPath:
    """Test XPath query engine."""

    def test_xpath_init(self):
        """Test XPath initialization."""
        xpath = XPath()
        assert repr(xpath) == "XPath()"

    def test_empty_query(self, sample_tree):
        """Test empty query raises error."""
        xpath = XPath()
        with pytest.raises(SearchError, match="XPath query cannot be empty"):
            xpath.query(sample_tree, "")

    def test_invalid_tree_type(self):
        """Test invalid tree type raises error."""
        xpath = XPath()
        with pytest.raises(SearchError, match="Tree must be an OrderedDict"):
            xpath.query({"key": "value"}, "/test")

    def test_absolute_path_single_key(self, sample_tree):
        """Test absolute path to single key."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/hostname")
        assert result.success
        assert result.data == "Router1"
        assert result.count == 1
        assert result.query == "/hostname"

    def test_absolute_path_nested(self, sample_tree):
        """Test absolute path to nested key."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/interface/GigabitEthernet0-0-1/ip/address")
        assert result.success
        assert result.data == "192.168.1.1 255.255.255.0"
        assert result.count == 1

    def test_absolute_path_dict(self, sample_tree):
        """Test absolute path returning dictionary."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/interface/GigabitEthernet0-0-1/ip")
        assert result.success
        assert isinstance(result.data, OrderedDict)
        assert "address" in result.data
        assert "nat" in result.data

    def test_absolute_path_not_found(self, sample_tree):
        """Test absolute path that doesn't exist."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/interface/GigabitEthernet0-0-99")
        assert not result.success
        assert result.count == 0

    def test_recursive_search(self, sample_tree):
        """Test recursive search finds all matches."""
        xpath = XPath()
        result = xpath.query(sample_tree, "//address")
        assert result.success
        assert result.count == 3  # Three interfaces with addresses
        assert "192.168.1.1" in result.matches[0]

    def test_recursive_search_nested(self, sample_tree):
        """Test recursive search for nested path."""
        xpath = XPath()
        result = xpath.query(sample_tree, "//ip/address")
        assert result.success
        assert result.count == 3

    def test_wildcard_single_level(self, sample_tree):
        """Test wildcard at single level."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/interface/*")
        # Should return interface names
        assert result.success
        assert result.count == 3
        assert "GigabitEthernet0-0-1" in result.matches
        assert "GigabitEthernet0-0-2" in result.matches
        assert "Loopback0" in result.matches

    def test_wildcard_with_continuation(self, sample_tree):
        """Test wildcard with path continuation."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/interface/*/description")
        assert result.success
        assert result.count == 3
        assert "WAN Interface" in result.matches
        assert "LAN Interface" in result.matches

    def test_wildcard_nested(self, sample_tree):
        """Test wildcard in nested path."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/interface/*/ip/address")
        assert result.success
        assert result.count == 3

    def test_predicate_exact_match(self, sample_tree):
        """Test predicate with exact match."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/interface[GigabitEthernet0-0-1]")
        assert result.success
        assert result.count == 1
        assert isinstance(result.data, OrderedDict)

    def test_predicate_wildcard(self, sample_tree):
        """Test predicate with wildcard pattern."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/interface[GigabitEthernet*]/ip/address")
        assert result.success
        assert result.count == 2  # Two GigabitEthernet interfaces
        assert "192.168.1.1" in result.matches[0]

    def test_predicate_wildcard_prefix(self, sample_tree):
        """Test predicate with wildcard prefix."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/interface[*0]/ip/address")
        assert result.success
        assert result.count == 1  # Only Loopback0

    def test_root_path(self, sample_tree):
        """Test root path returns entire tree."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/")
        assert result.success
        assert result.data == sample_tree

    def test_relative_path_treated_as_absolute(self, sample_tree):
        """Test relative path (no leading /) treated as absolute."""
        xpath = XPath()
        result = xpath.query(sample_tree, "hostname")
        assert result.success
        assert result.data == "Router1"

    def test_case_insensitive_matching(self, sample_tree):
        """Test pattern matching is case insensitive."""
        xpath = XPath()
        result = xpath.query(sample_tree, "/interface[gigabit*]")
        assert result.success
        assert result.count == 2


class TestParserXPath:
    """Test XPath integration with Parser class."""

    def test_parser_xpath_with_stored_tree(self, sample_tree):
        """Test Parser.xpath uses stored tree."""
        parser = Parser()
        parser.data = sample_tree  # Simulate parsed tree

        result = parser.xpath("//ip/address")
        assert result.success
        assert result.count == 3

    def test_parser_xpath_with_custom_tree(self, sample_tree):
        """Test Parser.xpath with custom tree parameter."""
        parser = Parser()
        # Don't set parser.data

        result = parser.xpath("//ip/address", tree=sample_tree)
        assert result.success
        assert result.count == 3

    def test_parser_xpath_no_tree(self):
        """Test Parser.xpath without tree data."""
        parser = Parser()

        result = parser.xpath("//test")
        assert not result.success
        assert "No tree data available" in result.error

    def test_parser_xpath_invalid_query(self, sample_tree):
        """Test Parser.xpath with invalid query."""
        parser = Parser()
        parser.data = sample_tree

        result = parser.xpath("")
        assert not result.success
        assert result.error is not None

    def test_parser_xpath_result_attributes(self, sample_tree):
        """Test XPathResult attributes."""
        parser = Parser()
        parser.data = sample_tree

        result = parser.xpath("/hostname")
        assert result.success
        assert result.data == "Router1"
        assert result.count == 1
        assert len(result.matches) == 1
        assert result.query == "/hostname"
        assert result.error is None

    def test_parser_xpath_boolean_evaluation(self, sample_tree):
        """Test XPathResult boolean evaluation."""
        parser = Parser()
        parser.data = sample_tree

        result = parser.xpath("/hostname")
        assert result  # Should evaluate to True

        result = parser.xpath("/nonexistent")
        assert not result  # Should evaluate to False

    def test_parser_workflow_integration(self, tmp_path):
        """Test complete workflow with file reading and parsing."""
        # Create test config file
        config_file = tmp_path / "config.txt"
        config_file.write_text(
            """interface GigabitEthernet0/0/1
  description WAN
  ip address 192.168.1.1 255.255.255.0
interface GigabitEthernet0/0/2
  description LAN
  ip address 10.0.0.1 255.255.255.0
hostname TestRouter
"""
        )

        parser = Parser()
        data = parser.read(str(config_file))
        parser.parse_tree(data)

        # Now use xpath - note the tree structure has full lines as keys
        result = parser.xpath("//description WAN")
        assert result.success
        assert result.count == 1

    def test_xpath_chaining(self, sample_tree):
        """Test chaining multiple xpath queries."""
        parser = Parser()
        parser.data = sample_tree

        # First query
        result1 = parser.xpath("/interface/GigabitEthernet0-0-1")
        assert result1.success

        # Query on result
        result2 = parser.xpath("/ip/address", tree=result1.data)
        assert result2.success
        assert "192.168.1.1" in result2.data


class TestXPathEdgeCases:
    """Test edge cases and complex scenarios."""

    def test_deep_nesting(self):
        """Test very deep nesting."""
        tree = OrderedDict(
            [("a", OrderedDict([("b", OrderedDict([("c", OrderedDict([("d", "value")]))]))]))]
        )
        xpath = XPath()
        result = xpath.query(tree, "/a/b/c/d")
        assert result.success
        assert result.data == "value"

    def test_empty_tree(self):
        """Test query on empty tree."""
        tree = OrderedDict()
        xpath = XPath()
        result = xpath.query(tree, "/test")
        assert not result.success

    def test_special_characters_in_keys(self):
        """Test keys with special characters."""
        tree = OrderedDict(
            [
                (
                    "interface-vlan-100",
                    OrderedDict(
                        [
                            ("ip_address", "10.0.0.1"),
                        ]
                    ),
                ),
            ]
        )
        xpath = XPath()
        result = xpath.query(tree, "/interface-vlan-100/ip_address")
        assert result.success
        assert result.data == "10.0.0.1"

    def test_numeric_keys(self):
        """Test numeric keys."""
        tree = OrderedDict(
            [
                (
                    "vlan",
                    OrderedDict(
                        [
                            ("100", OrderedDict([("name", "DATA")])),
                            ("200", OrderedDict([("name", "VOICE")])),
                        ]
                    ),
                ),
            ]
        )
        xpath = XPath()
        result = xpath.query(tree, "/vlan/100/name")
        assert result.success
        assert result.data == "DATA"

    def test_multiple_wildcard_levels(self):
        """Test multiple wildcards in path."""
        tree = OrderedDict(
            [
                (
                    "level1",
                    OrderedDict(
                        [
                            ("a", OrderedDict([("target", "value1")])),
                            ("b", OrderedDict([("target", "value2")])),
                        ]
                    ),
                ),
            ]
        )
        xpath = XPath()
        result = xpath.query(tree, "/level1/*/target")
        assert result.success
        assert result.count == 2
