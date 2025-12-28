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
from typing import Any, List, Optional

from .models import TableData, TableParseResult, TreeData, TreeParseResult
from .reader import Reader
from .search import Search
from .shsplit import ShowSplit
from .table_parser import TableParser
from .tree_parser import TreeParser


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

    def __init__(self, log_level: int = logging.INFO, log_format: Optional[str] = None) -> None:
        """Initialize the Parser.

        Args:
            log_level: Logging level (default: INFO)
            log_format: Custom log format string
        """
        # State for backward compatibility
        self.data: TreeData = OrderedDict()
        self.table: TableData = []

        # Logging
        self.format: Optional[str] = log_format
        self.logger: logging.Logger = self._set_logger_level(log_level)

        # Specialized components
        self.search: Search = Search()
        self.tree_parser: TreeParser = TreeParser()
        self.table_parser: TableParser = TableParser()

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

    def parse_tree(self, lines: List[str]) -> TreeData:
        """Parse hierarchical configuration into tree structure.

        Delegates to TreeParser for processing. Maintains state for
        backward compatibility.

        Args:
            lines: Configuration lines with indentation

        Returns:
            Nested OrderedDict representing configuration hierarchy

        Example:
            >>> parser = Parser()
            >>> config = ['interface Ethernet0', '  ip address 1.1.1.1']
            >>> tree = parser.parse_tree(config)
        """
        self.data = self.tree_parser.parse_tree(lines)
        return self.data

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
