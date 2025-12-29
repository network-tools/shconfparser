"""Tests for XPath functionality on YAML dict structures."""

import unittest

from shconfparser import Parser, XPathResult


class TestXPath(unittest.TestCase):
    """Test XPath queries on YAML format data."""

    def setUp(self):
        """Set up parser with YAML format and parse test data."""
        self.parser = Parser(output_format="yaml")
        lines = self.parser.read("data/shrun.txt")
        self.tree = self.parser.parse_tree(lines)

    def test_xpath_result_dataclass(self):
        """Test XPathResult dataclass structure."""
        result = self.parser.xpath("/hostname")
        self.assertIsInstance(result, XPathResult)
        self.assertTrue(hasattr(result, "success"))
        self.assertTrue(hasattr(result, "data"))
        self.assertTrue(hasattr(result, "matches"))
        self.assertTrue(hasattr(result, "count"))
        self.assertTrue(hasattr(result, "query"))
        self.assertTrue(hasattr(result, "error"))

    def test_xpath_result_bool(self):
        """Test XPathResult boolean evaluation."""
        result_success = self.parser.xpath("/hostname")
        result_failure = self.parser.xpath("/nonexistent")
        self.assertTrue(result_success)
        self.assertFalse(result_failure)

    def test_simple_absolute_path(self):
        """Test simple absolute path query."""
        result = self.parser.xpath("/hostname")
        self.assertTrue(result.success)
        self.assertEqual(result.data, "R1")
        self.assertEqual(result.count, 1)
        self.assertEqual(result.query, "/hostname")

    def test_nested_absolute_path(self):
        """Test nested absolute path query."""
        result = self.parser.xpath("/interface/FastEthernet0/0/duplex")
        # Should fail because FastEthernet0/0 requires predicate syntax
        self.assertFalse(result.success)

    def test_predicate_with_slash(self):
        """Test predicate syntax with identifier containing slash."""
        result = self.parser.xpath("/interface[FastEthernet0/0]")
        self.assertTrue(result.success)
        self.assertIsInstance(result.data, dict)
        self.assertIn("duplex", result.data)
        self.assertIn("ip", result.data)

    def test_predicate_with_continuation(self):
        """Test predicate followed by path continuation."""
        result = self.parser.xpath("/interface[FastEthernet0/0]/duplex")
        self.assertTrue(result.success)
        self.assertEqual(result.data, "auto")

    def test_deep_nested_with_predicate(self):
        """Test deep nested path with predicate."""
        result = self.parser.xpath("/interface[FastEthernet0/0]/ip/address")
        self.assertTrue(result.success)
        self.assertEqual(result.data, "1.1.1.1 255.255.255.0")

    def test_recursive_search(self):
        """Test recursive search (// operator)."""
        result = self.parser.xpath("//duplex")
        self.assertTrue(result.success)
        self.assertEqual(result.count, 2)
        self.assertIsInstance(result.matches, list)
        self.assertEqual(len(result.matches), 2)
        self.assertIn("auto", result.matches)

    def test_recursive_search_single_result(self):
        """Test recursive search returning single result."""
        result = self.parser.xpath("//hostname")
        self.assertTrue(result.success)
        self.assertEqual(result.count, 1)
        self.assertEqual(result.data, "R1")

    def test_wildcard_in_path(self):
        """Test wildcard (*) in path."""
        result = self.parser.xpath("/interface/*/duplex")
        self.assertTrue(result.success)
        self.assertEqual(result.count, 2)
        self.assertIsInstance(result.matches, list)
        self.assertEqual(len(result.matches), 2)

    def test_wildcard_in_predicate(self):
        """Test wildcard pattern in predicate."""
        result = self.parser.xpath("/interface[FastEthernet*]/duplex")
        self.assertTrue(result.success)
        self.assertEqual(result.count, 2)
        self.assertIsInstance(result.matches, list)

    def test_predicate_pattern_matching(self):
        """Test predicate with partial pattern match."""
        result = self.parser.xpath("/interface[*0/0]")
        self.assertTrue(result.success)
        self.assertIsInstance(result.data, dict)

    def test_nonexistent_path(self):
        """Test query for nonexistent path."""
        result = self.parser.xpath("/nonexistent")
        self.assertFalse(result.success)
        self.assertIsNone(result.data)
        self.assertEqual(result.count, 0)
        self.assertIsNone(result.error)

    def test_invalid_query_format(self):
        """Test invalid query format."""
        result = self.parser.xpath("invalid")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
        self.assertIn("must start with", result.error.lower())

    def test_empty_query(self):
        """Test empty query string."""
        result = self.parser.xpath("")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)

    def test_multiple_wildcards(self):
        """Test multiple wildcards in path."""
        result = self.parser.xpath("/interface/*/ip/*")
        self.assertTrue(result.success)
        self.assertGreater(result.count, 0)

    def test_xpath_on_json_format(self):
        """Test XPath on JSON format works (modern hierarchical format)."""
        parser = Parser(output_format="json")
        lines = parser.read("data/shrun.txt")
        parser.parse_tree(lines)
        result = parser.xpath("/hostname")
        # XPath works with modern json format
        self.assertTrue(result.success)
        self.assertEqual(result.data, "R1")

    def test_xpath_on_legacy_format(self):
        """Test XPath on legacy format (should return error)."""
        parser = Parser()  # Defaults to legacy
        lines = parser.read("data/shrun.txt")
        parser.parse_tree(lines)
        result = parser.xpath("/hostname")
        # XPath doesn't work with legacy format
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
        self.assertIn("modern format", result.error.lower())

    def test_predicate_exact_match(self):
        """Test predicate with exact identifier match."""
        result1 = self.parser.xpath("/interface[FastEthernet0/0]")
        result2 = self.parser.xpath("/interface[FastEthernet0/1]")
        self.assertTrue(result1.success)
        self.assertTrue(result2.success)
        self.assertNotEqual(result1.data, result2.data)

    def test_recursive_with_wildcard(self):
        """Test recursive search combined with wildcard."""
        result = self.parser.xpath("//ip/*")
        self.assertTrue(result.success)
        self.assertGreater(result.count, 0)

    def test_yaml_structure_preserved(self):
        """Test that YAML structure maintains clean format without nulls."""
        # Verify the tree doesn't have unnecessary null values
        self.assertIsInstance(self.tree, dict)
        if "hostname" in self.tree:
            # Should be string, not dict with null
            self.assertIsInstance(self.tree["hostname"], str)

    def test_two_level_split(self):
        """Test that leaf values are split max 2 levels deep."""
        result = self.parser.xpath("/interface[FastEthernet0/0]/ip/address")
        # Address should be a single string, not nested dict
        self.assertIsInstance(result.data, str)
        self.assertIn("1.1.1.1", result.data)

    def test_context_none(self):
        """Test context='none' returns just matched values."""
        result = self.parser.xpath("/interface/*/duplex", context="none")
        self.assertTrue(result.success)
        self.assertEqual(result.count, 2)
        # Should return just the values
        self.assertEqual(result.matches[0], "auto")
        self.assertEqual(result.matches[1], "auto")

    def test_context_partial(self):
        """Test context='partial' includes path from wildcard match."""
        result = self.parser.xpath("/interface/*/duplex", context="partial")
        self.assertTrue(result.success)
        self.assertEqual(result.count, 2)
        # Should include interface name
        self.assertIsInstance(result.matches[0], dict)
        self.assertIn("FastEthernet0/0", result.matches[0])
        self.assertEqual(result.matches[0]["FastEthernet0/0"]["duplex"], "auto")

    def test_context_full(self):
        """Test context='full' includes full tree hierarchy."""
        result = self.parser.xpath("/interface/*/duplex", context="full")
        self.assertTrue(result.success)
        self.assertEqual(result.count, 2)
        # Should include full path from root
        self.assertIsInstance(result.matches[0], dict)
        self.assertIn("interface", result.matches[0])
        self.assertIn("FastEthernet0/0", result.matches[0]["interface"])

    def test_context_with_predicate_wildcard(self):
        """Test context with predicate containing wildcard."""
        result = self.parser.xpath("/interface[FastEthernet*]/ip", context="partial")
        self.assertTrue(result.success)
        # Should show which FastEthernet interface
        self.assertIsInstance(result.data, dict)
        self.assertTrue("FastEthernet0/0" in result.data or "FastEthernet0/1" in result.data)

    def test_context_invalid(self):
        """Test invalid context parameter."""
        result = self.parser.xpath("/hostname", context="invalid")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
        self.assertIn("Invalid context", result.error)

    def test_paths_tracking(self):
        """Test that paths are tracked in results."""
        result = self.parser.xpath("/interface/*/duplex")
        self.assertTrue(result.success)
        self.assertEqual(len(result.paths), result.count)
        # Paths should contain path components
        for path in result.paths:
            self.assertIsInstance(path, list)
            self.assertIn("interface", path)
            self.assertIn("duplex", path)

    def test_context_recursive_search(self):
        """Test context with recursive search."""
        result = self.parser.xpath("//duplex", context="partial")
        self.assertTrue(result.success)
        self.assertGreater(result.count, 0)
        # With context, should show parent structure
        self.assertIsInstance(result.matches[0], dict)


if __name__ == "__main__":
    unittest.main()
