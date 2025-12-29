"""Parser module for network configuration parsing.

This module provides the main Parser class that orchestrates parsing of
network device show command outputs into structured data formats using
specialized sub-parsers.
"""

import json
import logging
import re
import sys
from collections import OrderedDict
from typing import Any, Dict, List, Optional

from .models import (
    TableData,
    TableParseResult,
    TreeData,
    TreeDataOrDict,
    TreeParseResult,
    XPathResult,
)
from .reader import Reader
from .search import Search
from .shsplit import ShowSplit
from .table_parser import TableParser
from .tree_parser import TreeParser
from .xpath import XPath


class Parser:
    """Main parser orchestrator for network configuration data.

    This class coordinates specialized parsers (TreeParser, TableParser) to
    handle various formats of network device output. It provides a unified
    interface while delegating specific parsing tasks to focused components.

    Attributes:
        name: Parser name identifier
        data: Parsed tree/data structure (for backward compatibility)
        table: Parsed table data (for backward compatibility)
        search: Search utility instance
        tree_parser: TreeParser instance
        table_parser: TableParser instance
    """

    name: str = "shconfparser"

    def __init__(
        self,
        log_level: int = logging.INFO,
        log_format: Optional[str] = None,
        output_format: Optional[str] = None,
    ) -> None:
        """Initialize the Parser.

        Args:
            log_level: Logging level (default: INFO)
            log_format: Custom log format string
            output_format: Output structure format
                - None or 'legacy' (default): OrderedDict with full command strings
                  Example: {'interface FastEthernet0/0': {'ip address 1.1.1.1': ''}}
                  For backward compatibility. No XPath support.

                - 'json': Hierarchical dict structure
                  Example: {'interface': {'FastEthernet0/0': {'ip': {'address': '1.1.1.1'}}}}
                  XPath support enabled. Clean programmatic access.

                - 'yaml': Hierarchical dict structure (same as json)
                  Example: {'interface': {'FastEthernet0/0': {'ip': {'address': '1.1.1.1'}}}}
                  XPath support enabled. YAML-friendly output.
        """
        # State for backward compatibility
        self.data: TreeData = OrderedDict()
        self.table: TableData = []

        # Output format configuration (None defaults to 'legacy' for backward compatibility)
        self.output_format: str = output_format if output_format is not None else "legacy"

        # Logging
        self.format: Optional[str] = log_format
        self.logger: logging.Logger = self._set_logger_level(log_level)

        # Specialized components
        self.search: Search = Search()
        self.tree_parser: TreeParser = TreeParser()
        self.table_parser: TableParser = TableParser()
        self.xpath_engine: XPath = XPath()

    def __repr__(self) -> str:
        """Return string representation for debugging."""
        return f"Parser(data_keys={len(self.data)}, table_rows={len(self.table)})"

    def _set_logger_level(self, log_level: int) -> logging.Logger:
        """Configure and return a logger instance.

        Args:
            log_level: Logging level to set

        Returns:
            Configured logger instance
        """
        if self.format is None:
            self.format = "[ %(levelname)s ] :: [ %(name)s ] :: %(message)s"
        logging.basicConfig(stream=sys.stdout, level=log_level, format=self.format, datefmt=None)
        logger = logging.getLogger(self.name)
        logger.setLevel(log_level)
        return logger

    def parse_tree(self, lines: List[str], format: Optional[str] = None) -> TreeDataOrDict:
        """Parse hierarchical configuration into tree structure.

        Delegates to TreeParser for processing. Maintains state for
        backward compatibility.

        Args:
            lines: Configuration lines with indentation
            format: Output format ('legacy', 'json', or 'yaml'). If None, uses self.output_format

        Returns:
            - 'legacy': OrderedDict with full command strings as keys
            - 'json' or 'yaml': dict with hierarchical structure

        Example:
            >>> parser = Parser()  # Defaults to 'legacy'
            >>> config = ['interface Ethernet0', '  ip address 1.1.1.1']
            >>> tree = parser.parse_tree(config)  # Returns OrderedDict with full keys

            >>> parser = Parser(output_format='json')
            >>> tree = parser.parse_tree(config)  # Returns dict with hierarchy
        """
        # Parse to OrderedDict first
        ordered_tree = self.tree_parser.parse_tree(lines)

        # Transform based on format
        output_format = format if format is not None else self.output_format

        # Validate format
        valid_formats = {"legacy", "json", "yaml"}
        if output_format not in valid_formats:
            raise ValueError(
                f"Invalid output_format '{output_format}'. "
                f"Must be one of: {', '.join(sorted(valid_formats))}"
            )

        if output_format == "legacy":
            # Legacy format: OrderedDict with full command strings
            self.data = ordered_tree
            return ordered_tree
        else:
            # Modern formats (json/yaml): dict with hierarchical structure
            hierarchical_tree = self._tree_to_yaml_structure(ordered_tree)
            self.data = hierarchical_tree  # type: ignore[assignment]
            return hierarchical_tree

    def parse_tree_safe(self, lines: List[str]) -> TreeParseResult:
        """Parse tree structure with structured result.

        Delegates to TreeParser and returns a structured result
        instead of raising exceptions.

        Args:
            lines: Configuration lines with indentation

        Returns:
            TreeParseResult with success status and data or error
        """
        result = self.tree_parser.parse_tree_safe(lines)
        if result.success and result.data:
            self.data = result.data
        return result

    def parse_data(self, lines: List[str]) -> TreeData:
        """Parse simple data lines into ordered dictionary.

        Args:
            lines: List of text lines

        Returns:
            OrderedDict with lines as keys

        Example:
            >>> parser = Parser()
            >>> data = parser.parse_data(['Router uptime is 5 days'])
        """
        self.data = OrderedDict()
        for line in lines:
            line = str(line).rstrip()
            self.data[line] = "None"
        return self.data

    def parse_table(
        self, lines: List[str], header_names: List[str], pattern: str = "#", re_escape: bool = True
    ) -> Optional[TableData]:
        """Parse tabular data into list of dictionaries.

        Delegates to TableParser for processing. Maintains state and
        returns None on error for backward compatibility.

        Args:
            lines: Lines containing table data
            header_names: List of column header names
            pattern: Pattern marking end of table (default: '#')
            re_escape: Whether to escape regex chars in headers (default: True)

        Returns:
            List of dictionaries (one per row), or None if header not found

        Example:
            >>> parser = Parser()
            >>> headers = ['Device ID', 'Interface', 'IP Address']
            >>> table = parser.parse_table(lines, headers)
        """
        try:
            # Validate inputs
            if not lines or not isinstance(lines, list):
                self.logger.error("Invalid lines input for parse_table")
                return None

            if not header_names or not isinstance(header_names, list):
                self.logger.error("Invalid header_names input for parse_table")
                return None

            # Build the pattern like old implementation for backward compatibility
            converted_headers = []
            for header in header_names:
                if re_escape:
                    converted_headers.append(re.escape(header))
                else:
                    converted_headers.append(header.replace(" ", r"\s+"))

            # Join with flexible spacing like old implementation
            header_pattern = r"\s+".join(converted_headers)
            header_pattern = r"\s*" + header_pattern

            # Use the table parser with built pattern
            self.table = self.table_parser.parse_table(
                lines, header_names, pattern, re_split=False, custom_pattern=header_pattern
            )
            return self.table
        except Exception as e:
            self.logger.error(f"Failed to parse table: {str(e)}")
            return None

    def parse_table_safe(
        self, lines: List[str], header_names: List[str], pattern: str = "#", re_escape: bool = True
    ) -> TableParseResult:
        """Parse table structure with structured result.

        Delegates to TableParser and returns a structured result
        instead of raising exceptions.

        Args:
            lines: Lines containing table data
            header_names: List of column header names
            pattern: Pattern marking end of table
            re_escape: Whether to escape regex chars in headers

        Returns:
            TableParseResult with success status and data or error
        """
        result = self.table_parser.parse_table_safe(lines, header_names, pattern, re_escape)
        if result.success and result.data:
            self.table = result.data
        return result

    def split(
        self, lines: List[str], pattern: Optional[str] = None
    ) -> Optional[OrderedDict[str, List[str]]]:
        """Split show command output into separate commands.

        Args:
            lines: Combined output lines
            pattern: Regex pattern to identify commands

        Returns:
            OrderedDict mapping command names to their output lines, or None if empty
        """
        self.s = ShowSplit()  # For backward compatibility
        return self.s.split(lines, pattern)

    def read(self, path: str) -> Optional[List[str]]:
        """Read file contents.

        Args:
            path: File path to read

        Returns:
            List of lines from file, or None if file doesn't exist
        """
        self.r = Reader(path)  # For backward compatibility
        return self.r.data

    def dump(self, data: Any, indent: Optional[int] = None) -> str:
        """Convert data to JSON string.

        Args:
            data: Data structure to serialize
            indent: Number of spaces for indentation

        Returns:
            JSON string representation
        """
        return json.dumps(data, indent=indent)

    def _tree_to_yaml_structure(self, tree: TreeData) -> Dict[str, Any]:
        """Transform OrderedDict tree to YAML-friendly structure.

        Converts flat keys into nested dict structure with smart depth limiting:
        - Containers (OrderedDict): Split fully, last word = identifier
        - Leaves (empty string): Max 2 levels, rest = value

        Examples:
            "interface FastEthernet0/0" (container) →
                {"interface": {"FastEthernet0/0": {...}}}

            "hostname R1" (leaf) →
                {"hostname": "R1"}

            "ip address 1.1.1.1 255.255.255.0" (leaf) →
                {"ip": {"address": "1.1.1.1 255.255.255.0"}}

        Args:
            tree: OrderedDict tree from parse_tree

        Returns:
            Nested dict suitable for YAML serialization
        """
        result: Dict[str, Any] = {}

        for key, value in tree.items():
            # Split key by spaces
            parts = key.split()

            if len(parts) == 1:
                # Single word key
                if isinstance(value, OrderedDict):
                    result[key] = self._tree_to_yaml_structure(value)
                else:
                    result[key] = value if value else None

            elif isinstance(value, OrderedDict):
                # Container with nested OrderedDict - split fully
                # Last word becomes identifier, rest is path
                *path_parts, identifier = parts

                # Build nested structure
                current: Dict[str, Any] = result
                for part in path_parts:
                    if part not in current:
                        current[part] = {}
                    current = current[part]

                # Add the identifier with its nested value
                current[identifier] = self._tree_to_yaml_structure(value)

            else:
                # Leaf value (empty string) - limit to 2 levels max
                if len(parts) == 2:
                    # Two words: first is key, second is value
                    # "hostname R1" → hostname: R1
                    # "duplex auto" → duplex: auto
                    result[parts[0]] = parts[1]

                elif len(parts) > 2:
                    # More than 2 words: first is level 1, second is level 2, rest is value
                    # "ip address 1.1.1.1 255.255.255.0" →
                    #   ip: {address: "1.1.1.1 255.255.255.0"}
                    level1, level2 = parts[0], parts[1]
                    value_str = " ".join(parts[2:])

                    if level1 not in result:
                        result[level1] = {}
                    elif not isinstance(result[level1], dict):
                        # Key exists as non-dict, convert to dict
                        result[level1] = {}
                    result[level1][level2] = value_str

        return result

    def xpath(
        self, query: str, tree: Optional[Dict[str, Any]] = None, context: str = "none"
    ) -> XPathResult:
        """Execute XPath-style query on YAML configuration tree.

        XPath queries work on YAML format (dict) trees. If tree is not provided,
        uses self.data. For best results, parse with output_format='yaml'.

        Supports:
        - Absolute paths: /interface/FastEthernet0/0/duplex
        - Recursive search: //duplex (find anywhere)
        - Wildcards: /interface/*/duplex
        - Predicates: /interface[FastEthernet0/0]

        Args:
            query: XPath-style query string
            tree: Optional dict tree to search (uses self.data if not provided)
            context: How much context to include in matches:
                - 'none': Just matched values (default)
                - 'partial': From wildcard match point to value
                - 'full': Full tree hierarchy from root

        Returns:
            XPathResult with matches, count, and metadata

        Example:
            >>> p = Parser(output_format='yaml')
            >>> lines = p.read('config.txt')
            >>> p.parse_tree(lines)
            >>> result = p.xpath('/interface/FastEthernet0/0/duplex')
            >>> result.data  # 'auto'
            >>> result = p.xpath('/interface/*/duplex', context='partial')
            >>> # Shows which interface each match came from
        """
        search_tree = tree if tree is not None else self.data

        if not search_tree:
            self.logger.warning("No tree data available for XPath query")
            return XPathResult(
                success=False,
                error="No tree data available. Parse a tree first or provide tree parameter.",
                query=query,
            )

        # XPath only works with modern formats (json/yaml)
        if self.output_format not in ("json", "yaml"):
            return XPathResult(
                success=False,
                error=(
                    f"XPath queries require modern format. Use output_format='json' or 'yaml'. "
                    f"Current format is '{self.output_format}' (OrderedDict with full command strings)."
                ),
                query=query,
            )

        # Ensure search_tree is a dict
        if not isinstance(search_tree, dict):
            self.logger.warning(
                "XPath requires dict structure. " f"Got {type(search_tree).__name__}."
            )
            return XPathResult(
                success=False,
                error=f"XPath requires dict structure, got {type(search_tree).__name__}",
                query=query,
            )

        try:
            return self.xpath_engine.query(search_tree, query, context)
        except Exception as e:
            self.logger.error(f"XPath query failed: {str(e)}")
            return XPathResult(success=False, error=str(e), query=query)
