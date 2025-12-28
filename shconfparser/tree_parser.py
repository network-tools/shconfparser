"""Tree parser for hierarchical configuration structures.

This module provides the TreeParser class for parsing hierarchical
configuration data (like Cisco configs) into nested dictionary structures.
"""

import logging
from collections import OrderedDict
from typing import Any, Dict, List

from .exceptions import TreeParseError, ValidationError
from .models import TreeData, TreeParseResult

logger = logging.getLogger(__name__)


class TreeParser:
    """Parser for hierarchical tree structures.

    This class handles parsing of indented configuration data into
    nested OrderedDict structures, maintaining the hierarchy.
    """

    def __init__(self) -> None:
        """Initialize the TreeParser."""
        pass

    def __repr__(self) -> str:
        """Return string representation for debugging."""
        return "TreeParser()"

    def _space_level(self, line: str) -> int:
        """Calculate indentation level of a line.

        Handles both spaces and tabs. Tabs are converted to 4 spaces.

        Args:
            line: Input line string

        Returns:
            Number of leading spaces (tabs count as 4)
        """
        # Convert tabs to spaces for consistent handling
        expanded_line = line.expandtabs(4)
        return len(expanded_line) - len(expanded_line.lstrip())

    def _convert_to_dict(self, tree: List[Dict[str, Any]], level: int = 0) -> TreeData:
        """Convert hierarchical tree structure to nested dictionary.

        Args:
            tree: List of nodes with 'key' and 'level' attributes
            level: Current indentation level

        Returns:
            Nested OrderedDict representing the hierarchy
        """
        temp_dict: TreeData = OrderedDict()
        for i, node in enumerate(tree):
            try:
                next_node = tree[i + 1]
            except IndexError:
                next_node = {"level": -1}

            if node["level"] > level:
                continue
            if node["level"] < level:
                return temp_dict

            if next_node["level"] == level:
                temp_dict[node["key"]] = ""
            elif next_node["level"] > level:
                temp_dict[node["key"]] = self._convert_to_dict(
                    tree[i + 1 :], level=next_node["level"]
                )
            else:
                temp_dict[node["key"]] = ""
                return temp_dict
        return temp_dict

    def _calculate_depth(self, tree: TreeData, current_depth: int = 0) -> int:
        """Calculate maximum depth of tree structure.

        Args:
            tree: Tree structure to analyze
            current_depth: Current depth level

        Returns:
            Maximum depth of the tree
        """
        max_depth = current_depth
        for value in tree.values():
            if isinstance(value, OrderedDict):
                depth = self._calculate_depth(value, current_depth + 1)
                max_depth = max(max_depth, depth)
        return max_depth

    def parse_tree(self, lines: List[str]) -> TreeData:
        """Parse hierarchical configuration into tree structure.

        This is a pure function that takes lines and returns a tree structure
        without maintaining state.

        Args:
            lines: Configuration lines with indentation

        Returns:
            Nested OrderedDict representing configuration hierarchy

        Raises:
            TreeParseError: If parsing fails
            ValidationError: If input data is invalid

        Example:
            >>> parser = TreeParser()
            >>> config = ['interface Ethernet0', '  ip address 1.1.1.1']
            >>> tree = parser.parse_tree(config)
        """
        if not lines:
            raise ValidationError("Input lines cannot be empty")

        if not isinstance(lines, list):
            raise ValidationError(f"Expected list, got {type(lines)}")

        try:
            data: List[Dict[str, Any]] = []
            for line in lines:
                space = self._space_level(line.rstrip())
                line = line.strip()
                if line not in ("!", "", "end"):
                    data.append({"key": line, "level": space})

            if not data:
                raise ValidationError("No valid data lines found")

            return self._convert_to_dict(data)

        except Exception as e:
            if isinstance(e, (TreeParseError, ValidationError)):
                raise
            raise TreeParseError(f"Failed to parse tree structure: {str(e)}") from e

    def parse_tree_safe(self, lines: List[str]) -> TreeParseResult:
        """Parse tree structure with structured result.

        This method wraps parse_tree() to return a structured result
        instead of raising exceptions.

        Args:
            lines: Configuration lines with indentation

        Returns:
            TreeParseResult with success status and data or error
        """
        try:
            tree = self.parse_tree(lines)
            depth = self._calculate_depth(tree)
            return TreeParseResult(success=True, data=tree, depth=depth)
        except ValidationError as e:
            return TreeParseResult(success=False, error=f"Validation error: {str(e)}")
        except TreeParseError as e:
            return TreeParseResult(success=False, error=str(e))
        except Exception as e:
            logger.exception("Unexpected error during tree parsing")
            return TreeParseResult(success=False, error=f"Unexpected error: {str(e)}")
