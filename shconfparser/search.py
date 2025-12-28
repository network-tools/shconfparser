"""Search module for finding patterns in parsed data.

This module provides the Search class for searching patterns in tree and
table structures.
"""

import re
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Pattern, Union

# Type aliases
TreeData = OrderedDict[str, Union[str, "TreeData"]]
TableRow = Dict[str, str]
TableData = List[TableRow]


class Search:
    """Search utility for parsed network configuration data.

    Provides methods to search for patterns in both tree structures
    (hierarchical configs) and table structures (show command tables).
    """

    def __init__(self) -> None:
        """Initialize the Search utility."""
        pass

    def __repr__(self) -> str:
        """Return string representation for debugging."""
        return "Search()"

    def validate(self, data: Any, dtype: type = OrderedDict) -> bool:
        """Validate data type and content.

        Args:
            data: Data to validate
            dtype: Expected data type (default: OrderedDict)

        Returns:
            True if valid, False otherwise
        """
        if data is None:
            return False
        return isinstance(data, dtype)

    def get_pattern(self, pattern: Union[str, Pattern[str]], strip: bool = True) -> Pattern[str]:
        """Convert string to compiled regex pattern with error handling.

        Args:
            pattern: String or compiled regex pattern
            strip: Whether to strip whitespace from string pattern

        Returns:
            Compiled regex pattern

        Raises:
            ValueError: If pattern is invalid type
            re.error: If regex compilation fails
        """
        # Check if already a compiled pattern
        if isinstance(pattern, re.Pattern):
            return pattern

        if not isinstance(pattern, str):
            raise ValueError(f"Pattern must be str or compiled regex, got {type(pattern)}")

        if strip:
            pattern = pattern.strip()

        try:
            return re.compile(pattern)
        except re.error as e:
            raise re.error(f"Invalid regex pattern '{pattern}': {e}")

    def search_in_tree(
        self, pattern: Union[str, Pattern[str]], data: Optional[TreeData] = None
    ) -> Optional[re.Match[str]]:
        """Search for first pattern match in tree structure.

        Args:
            pattern: Regex pattern to search for
            data: Tree data structure to search

        Returns:
            First match object, or None if not found
        """
        if not self.validate(data) or data is None:
            return None

        p = self.get_pattern(pattern)
        for key in data:
            res = p.match(key)
            if res:
                return res
        return None

    def search_all_in_tree(
        self, pattern: Union[str, Pattern[str]], data: Optional[TreeData] = None
    ) -> Optional[OrderedDict[re.Match[str], str]]:
        """Search for all pattern matches in tree structure.

        Args:
            pattern: Regex pattern to search for
            data: Tree data structure to search

        Returns:
            OrderedDict mapping match objects to keys, or None if no matches
        """
        if not self.validate(data) or data is None:
            return None

        p = self.get_pattern(pattern)
        match: OrderedDict[re.Match[str], str] = OrderedDict()
        for key in data:
            res = p.match(key)
            if res:
                match[res] = key
        return match if len(match) else None

    def search_in_tree_level(
        self, pattern: Union[str, Pattern[str]], data: Optional[TreeData] = None, level: int = 0
    ) -> Optional[str]:
        """Search for pattern in tree with depth limit.

        Args:
            pattern: Regex pattern to search for
            data: Tree data structure to search
            level: Maximum depth to search (0 = current level only)

        Returns:
            First matching key, or None if not found
        """
        if not self.validate(data) or data is None:
            return None

        p = self.get_pattern(pattern)
        for key in data:
            if p.match(key):
                return key
            value = data[key]
            if value is None:
                continue
            if isinstance(value, OrderedDict) and level > 0:
                res = self.search_in_tree_level(p, value, level=level - 1)
                if res:
                    return res
        return None

    def search_in_table(
        self,
        pattern: Union[str, Pattern[str]],
        data: Optional[TableData] = None,
        header_column: Optional[str] = None,
    ) -> Optional[TableRow]:
        """Search for pattern in table structure.

        Args:
            pattern: Regex pattern to search for
            data: Table data (list of dicts) to search
            header_column: Column name to search in

        Returns:
            First matching row dict, or None if not found
        """
        if not self.validate(data, dtype=list) or data is None or header_column is None:
            return None

        p = self.get_pattern(pattern)
        for each_row in data:
            if p.match(each_row[header_column]):
                return each_row
        return None

    def search_all_in_table(
        self,
        pattern: Union[str, Pattern[str]],
        data: Optional[TableData] = None,
        header_column: Optional[str] = None,
    ) -> Optional[TableData]:
        """Search for all pattern matches in table structure.

        Args:
            pattern: Regex pattern to search for
            data: Table data (list of dicts) to search
            header_column: Column name to search in

        Returns:
            List of matching row dicts, or None if no matches
        """
        if not self.validate(data, dtype=list) or data is None or header_column is None:
            return None

        p = self.get_pattern(pattern)
        match: TableData = []
        for each_row in data:
            if p.match(each_row[header_column]):
                match.append(each_row)
        return match if len(match) else None
