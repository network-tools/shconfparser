"""Protocol definitions for shconfparser.

This module provides protocol (interface) definitions for extensibility
and type-safe duck typing throughout the library.
"""

from collections import OrderedDict
from typing import Any, Dict, List, Optional, Protocol


class Parsable(Protocol):
    """Protocol for parsable objects."""

    def parse(self, lines: List[str]) -> Any:
        """Parse input lines into structured data.

        Args:
            lines: Input lines to parse

        Returns:
            Parsed data structure
        """
        ...


class TreeParsable(Protocol):
    """Protocol for tree-structure parsers."""

    def parse_tree(self, lines: List[str]) -> OrderedDict[str, Any]:
        """Parse hierarchical tree structure.

        Args:
            lines: Input lines with indentation hierarchy

        Returns:
            Nested OrderedDict representing the hierarchy
        """
        ...


class TableParsable(Protocol):
    """Protocol for table-structure parsers."""

    def parse_table(
        self,
        lines: List[str],
        header_keys: List[str],
        pattern: str = "",
        re_split: bool = False,
    ) -> List[Dict[str, str]]:
        """Parse table structure with headers and rows.

        Args:
            lines: Input lines containing table data
            header_keys: Expected header column names
            pattern: Pattern to identify end of table
            re_split: Whether to use regex splitting

        Returns:
            List of dictionaries representing table rows
        """
        ...


class Searchable(Protocol):
    """Protocol for searchable data structures."""

    def search(self, pattern: str, data: Any) -> Optional[Any]:
        """Search for pattern in data.

        Args:
            pattern: Search pattern (string or regex)
            data: Data structure to search

        Returns:
            First match or None
        """
        ...


class Splittable(Protocol):
    """Protocol for command splitters."""

    def split(
        self, lines: Optional[List[str]], pattern: Optional[str] = None
    ) -> Optional[OrderedDict[str, List[str]]]:
        """Split combined output into separate commands.

        Args:
            lines: Combined output lines
            pattern: Pattern to identify commands

        Returns:
            OrderedDict mapping command names to output lines
        """
        ...


class Readable(Protocol):
    """Protocol for file readers."""

    def read(self, path: str) -> Optional[List[str]]:
        """Read file content.

        Args:
            path: File or directory path

        Returns:
            List of lines or None if failed
        """
        ...


class Validatable(Protocol):
    """Protocol for data validators."""

    def validate(self, data: Any, dtype: type = OrderedDict) -> bool:
        """Validate data structure.

        Args:
            data: Data to validate
            dtype: Expected data type

        Returns:
            True if valid, False otherwise
        """
        ...
