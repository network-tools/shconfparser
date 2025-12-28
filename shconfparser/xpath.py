"""XPath-like query engine for parsed configuration trees.

This module provides XPath-style querying capabilities for navigating
and searching through parsed network configuration data structures.
"""

import logging
import re
from collections import OrderedDict
from typing import Any, List

from .exceptions import SearchError
from .models import TreeData, XPathResult

logger = logging.getLogger(__name__)


class XPath:
    """XPath-like query engine for configuration trees.

    Supports:
    - Absolute paths: /interface/GigabitEthernet0-0-1/ip/address
    - Relative paths: //ip/address (find anywhere)
    - Wildcards: /interface/*/ip
    - Get all keys: /interface/* (list all interfaces)
    - Predicates: /interface[GigabitEthernet*]

    Example:
        >>> xpath = XPath()
        >>> results = xpath.query(tree, '//ip/address')
        >>> result = xpath.query(tree, '/interface/GigabitEthernet0-0-1')
    """

    def __init__(self) -> None:
        """Initialize XPath engine."""
        pass

    def __repr__(self) -> str:
        """Return string representation."""
        return "XPath()"

    def query(self, tree: TreeData, path: str) -> XPathResult:
        """Execute XPath query on configuration tree.

        Args:
            tree: Parsed configuration tree (OrderedDict)
            path: XPath-style query string

        Returns:
            XPathResult with found data and metadata

        Raises:
            SearchError: If path syntax is invalid
        """
        if not path:
            raise SearchError("XPath query cannot be empty")

        if not isinstance(tree, OrderedDict):
            raise SearchError("Tree must be an OrderedDict")

        # Normalize path
        path = path.strip()

        # Handle different path types
        if path.startswith("//"):
            # Recursive search
            return self._search_recursive(tree, path[2:])
        elif path.startswith("/"):
            # Absolute path
            return self._search_absolute(tree, path[1:])
        else:
            # Relative path (treat as absolute)
            return self._search_absolute(tree, path)

    def _search_absolute(self, tree: TreeData, path: str) -> XPathResult:
        """Search using absolute path from root.

        Args:
            tree: Configuration tree
            path: Path without leading /

        Returns:
            XPathResult with matches
        """
        if not path:
            return XPathResult(success=True, data=tree, matches=[tree], count=1, query=f"/{path}")

        parts = self._split_path(path)
        matches = self._traverse_path(tree, parts, [])

        return XPathResult(
            success=len(matches) > 0,
            data=matches[0] if matches else None,
            matches=matches,
            count=len(matches),
            query=f"/{path}",
        )

    def _search_recursive(self, tree: TreeData, path: str) -> XPathResult:
        """Search recursively through entire tree.

        Args:
            tree: Configuration tree
            path: Path to search for

        Returns:
            XPathResult with all matches
        """
        parts = self._split_path(path)
        all_matches: List[Any] = []

        def recurse(node: Any, depth: int = 0) -> None:
            """Recursively search tree for matching paths."""
            if not isinstance(node, OrderedDict):
                return

            # Try to match from this node
            matches = self._traverse_path(node, parts, [])
            all_matches.extend(matches)

            # Recurse into children
            for value in node.values():
                if isinstance(value, OrderedDict):
                    recurse(value, depth + 1)

        recurse(tree)

        return XPathResult(
            success=len(all_matches) > 0,
            data=all_matches[0] if all_matches else None,
            matches=all_matches,
            count=len(all_matches),
            query=f"//{path}",
        )

    def _split_path(self, path: str) -> List[str]:
        """Split path into components.

        Args:
            path: XPath string

        Returns:
            List of path components
        """
        # Handle empty path
        if not path:
            return []

        # Split by / but preserve predicates [...]
        parts = []
        current = ""
        in_predicate = False

        for char in path:
            if char == "[":
                in_predicate = True
                current += char
            elif char == "]":
                in_predicate = False
                current += char
            elif char == "/" and not in_predicate:
                if current:
                    parts.append(current)
                current = ""
            else:
                current += char

        if current:
            parts.append(current)

        return parts

    def _traverse_path(
        self, tree: TreeData, parts: List[str], current_path: List[str]
    ) -> List[Any]:
        """Traverse tree following path components.

        Args:
            tree: Current node in tree
            parts: Remaining path components
            current_path: Path traversed so far

        Returns:
            List of matches
        """
        if not parts:
            return [tree]

        if not isinstance(tree, OrderedDict):
            return []

        part = parts[0]
        remaining = parts[1:]
        matches: List[Any] = []

        # Handle wildcards
        if part == "*":
            # Return all keys at this level if no more parts
            if not remaining:
                return list(tree.keys())
            # Otherwise traverse all children
            for key, value in tree.items():
                if isinstance(value, OrderedDict):
                    child_matches = self._traverse_path(value, remaining, current_path + [key])
                    matches.extend(child_matches)
                elif not remaining:  # Leaf node
                    matches.append(value)
            return matches

        # Handle predicates [pattern]
        if "[" in part:
            key_pattern, predicate = self._parse_predicate(part)

            # Check if key exists in tree
            if key_pattern in tree:
                value = tree[key_pattern]

                # If value is OrderedDict, filter its children by predicate
                if isinstance(value, OrderedDict):
                    for child_key, child_value in value.items():
                        if self._match_key(child_key, predicate):
                            if not remaining:
                                matches.append(child_value)
                            elif isinstance(child_value, OrderedDict):
                                child_matches = self._traverse_path(
                                    child_value, remaining, current_path + [key_pattern, child_key]
                                )
                                matches.extend(child_matches)
            return matches

        # Direct key lookup
        if part in tree:
            value = tree[part]
            if not remaining:
                return [value]
            if isinstance(value, OrderedDict):
                return self._traverse_path(value, remaining, current_path + [part])

        # Try pattern matching on keys
        for key, value in tree.items():
            if self._match_key(key, part):
                if not remaining:
                    matches.append(value)
                elif isinstance(value, OrderedDict):
                    child_matches = self._traverse_path(value, remaining, current_path + [key])
                    matches.extend(child_matches)

        return matches

    def _parse_predicate(self, part: str) -> tuple[str, str]:
        """Parse predicate from path component.

        Args:
            part: Path component with predicate like 'interface[Gig*]'

        Returns:
            Tuple of (key_pattern, predicate_pattern)
        """
        match = re.match(r"^([^\[]+)\[([^\]]+)\]$", part)
        if match:
            return match.group(1), match.group(2)
        return part, ""

    def _check_predicate(self, key: str, _value: Any, predicate: str) -> bool:
        """Check if key/value matches predicate.

        Args:
            key: Dictionary key
            _value: Dictionary value (unused but kept for future use)
            predicate: Predicate pattern

        Returns:
            True if matches
        """
        if not predicate:
            return True
        return self._match_key(key, predicate)

    def _match_key(self, key: str, pattern: str) -> bool:
        """Match key against pattern with wildcard support.

        Args:
            key: Dictionary key to match
            pattern: Pattern (supports * wildcard)

        Returns:
            True if key matches pattern
        """
        # Convert glob pattern to regex
        regex_pattern = pattern.replace("*", ".*")
        regex_pattern = f"^{regex_pattern}$"
        return bool(re.match(regex_pattern, key, re.IGNORECASE))
