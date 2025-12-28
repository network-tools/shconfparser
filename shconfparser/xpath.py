"""XPath-style query engine for YAML/dict configuration trees with context tracking.

This module provides XPath-like querying capabilities for parsed network
configurations in YAML format (dict structures).
"""

import re
from typing import Any, Dict, List, Optional, Tuple

from .models import XPathResult


class XPath:
    """XPath-style query engine for YAML dict structures.

    Supports NSO-style XPath queries on clean hierarchical dict structures
    with optional context tracking for wildcard matches.

    Examples:
        >>> xpath = XPath()
        >>> tree = {'interface': {'FastEthernet0/0': {'duplex': 'auto'}}}
        >>> result = xpath.query(tree, '/interface/FastEthernet0/0/duplex')
        >>> result.data  # 'auto'
        >>> result = xpath.query(tree, '/interface/*/duplex', context='partial')
        >>> result.matches  # [{'FastEthernet0/0': {'duplex': 'auto'}}]
    """

    def __init__(self) -> None:
        """Initialize XPath engine."""
        pass

    def __repr__(self) -> str:
        """Return string representation."""
        return "XPath()"

    def query(self, tree: Dict[str, Any], query: str, context: str = "none") -> XPathResult:
        """Execute XPath-style query on dict tree.

        Args:
            tree: Dictionary tree to search
            query: XPath query string
            context: How much context to include in matches:
                - 'none': Just matched values (default)
                - 'partial': From wildcard match point to value
                - 'full': Full tree hierarchy from root

        Returns:
            XPathResult with matches and metadata

        Examples:
            >>> result = xpath.query(tree, '/interface/FastEthernet0/0/duplex')
            >>> result = xpath.query(tree, '//duplex', context='partial')
            >>> result = xpath.query(tree, '/interface/*/duplex', context='full')
            >>> result = xpath.query(tree, '/interface[FastEthernet*]', context='partial')
        """
        if not query:
            return XPathResult(
                success=False,
                error="XPath query cannot be empty",
                query=query,
            )

        # Validate query format
        if not (query.startswith("/") or query.startswith("//")):
            return XPathResult(
                success=False,
                error="XPath query must start with / or //",
                query=query,
            )

        if not isinstance(tree, dict):
            return XPathResult(
                success=False,
                error=f"Tree must be a dict, got {type(tree).__name__}",
                query=query,
            )

        # Validate context parameter
        if context not in ("none", "partial", "full"):
            return XPathResult(
                success=False,
                error=f"Invalid context '{context}'. Must be 'none', 'partial', or 'full'",
                query=query,
            )

        try:
            # Handle root path
            if query == "/":
                return XPathResult(
                    success=True,
                    data=tree,
                    matches=[tree],
                    count=1,
                    query=query,
                    paths=[[]],
                )

            # Parse query
            is_recursive = query.startswith("//")
            path = query.lstrip("/")

            if is_recursive:
                # Recursive search with path tracking
                matches, paths = self._search_recursive_with_paths(tree, path, [])
            else:
                # Absolute path with path tracking
                matches, paths = self._search_absolute_with_paths(tree, path, [])

            if matches:
                # Apply context if needed
                if context != "none" and paths:
                    final_matches = [
                        self._build_context(match, path_components, context)
                        for match, path_components in zip(matches, paths)
                    ]
                else:
                    final_matches = matches

                return XPathResult(
                    success=True,
                    data=final_matches[0] if final_matches else None,
                    matches=final_matches,
                    count=len(final_matches),
                    query=query,
                    paths=paths,
                )
            else:
                return XPathResult(
                    success=False,
                    data=None,
                    matches=[],
                    count=0,
                    query=query,
                    paths=[],
                )

        except Exception as e:
            return XPathResult(
                success=False,
                error=f"XPath query failed: {str(e)}",
                query=query,
            )

    def _build_context(self, match: Any, path: List[str], context_type: str) -> Any:
        """Build context structure around a match.

        Args:
            match: The matched value
            path: Full path components from root to match
            context_type: 'partial' or 'full'

        Returns:
            Dict with context hierarchy or original match value

        For 'partial' context with path ['interface', 'FastEthernet0/0', 'ip']:
            Returns: {'FastEthernet0/0': {'ip': match}}
        For 'full' context:
            Returns: {'interface': {'FastEthernet0/0': {'ip': match}}}
        """
        if context_type == "none" or not path:
            return match

        # For partial context, skip the first component (container level)
        # This shows from the wildcard/predicate match point
        if context_type == "partial":  # noqa: SIM108
            path_to_use = path[1:] if len(path) > 1 else path
        else:
            path_to_use = path

        # Build nested dict from path
        if not path_to_use:
            return match

        result = match
        for component in reversed(path_to_use):
            result = {component: result}

        return result

    def _search_absolute_with_paths(
        self, tree: Dict[str, Any], path: str, current_path: List[str]
    ) -> Tuple[List[Any], List[List[str]]]:
        """Search using absolute path, tracking paths to matches.

        Args:
            tree: Current dict to search
            path: Path segments (without leading /)
            current_path: Path components from root to current position

        Returns:
            Tuple of (matches list, paths list)
        """
        segments = self._parse_path(path)

        if not segments:
            return [tree], [current_path]

        return self._traverse_path_with_tracking(tree, segments, current_path)

    def _search_recursive_with_paths(
        self, tree: Dict[str, Any], pattern: str, current_path: List[str]
    ) -> Tuple[List[Any], List[List[str]]]:
        """Recursively search for pattern anywhere in tree, tracking paths.

        Args:
            tree: Current dict to search
            pattern: Pattern to match
            current_path: Path components from root to current position

        Returns:
            Tuple of (matches list, paths list)
        """
        all_matches = []
        all_paths = []

        # Try to match at current level
        current_matches, current_match_paths = self._search_absolute_with_paths(
            tree, pattern, current_path
        )
        all_matches.extend(current_matches)
        all_paths.extend(current_match_paths)

        # Recursively search in nested dicts
        for key, value in tree.items():
            if isinstance(value, dict):
                nested_path = current_path + [key]
                nested_matches, nested_paths = self._search_recursive_with_paths(
                    value, pattern, nested_path
                )
                all_matches.extend(nested_matches)
                all_paths.extend(nested_paths)

        return all_matches, all_paths

    def _parse_path(self, path: str) -> List[Tuple[str, Optional[str]]]:
        """Parse path into segments with predicates.

        Args:
            path: Path string like "interface/FastEthernet0/0" or "interface[FastEthernet0/0]"

        Returns:
            List of (segment, predicate) tuples
        """
        segments = []
        predicate_pattern = r"([^/\[]+)\[([^\]]+)\]"

        parts = []
        current_pos = 0

        while current_pos < len(path):
            match = re.search(predicate_pattern, path[current_pos:])

            if match:
                before = path[current_pos : current_pos + match.start()]
                if before:
                    parts.extend([p for p in before.split("/") if p])

                segment = match.group(1)
                predicate = match.group(2)
                segments.append((segment, predicate))

                current_pos += match.end()

                if current_pos < len(path) and path[current_pos] == "/":
                    current_pos += 1
            else:
                remaining = path[current_pos:]
                parts.extend([p for p in remaining.split("/") if p])
                break

        for part in parts:
            if part:
                segments.append((part, None))

        return segments

    def _traverse_path_with_tracking(
        self,
        tree: Dict[str, Any],
        segments: List[Tuple[str, Optional[str]]],
        current_path: List[str],
    ) -> Tuple[List[Any], List[List[str]]]:
        """Traverse path through tree, tracking paths to matches.

        Args:
            tree: Current dict
            segments: List of (segment, predicate) tuples
            current_path: Path components from root to current position

        Returns:
            Tuple of (matches list, paths list)
        """
        if not segments:
            return [tree], [current_path]

        current_segment, predicate = segments[0]
        remaining_segments = segments[1:]

        all_matches = []
        all_paths = []

        # Handle wildcards
        if "*" in current_segment:
            pattern = current_segment.replace("*", ".*")
            for key, value in tree.items():
                if re.match(pattern, str(key), re.IGNORECASE):
                    new_path = current_path + [key]
                    if remaining_segments:
                        if isinstance(value, dict):
                            nested_matches, nested_paths = self._traverse_path_with_tracking(
                                value, remaining_segments, new_path
                            )
                            all_matches.extend(nested_matches)
                            all_paths.extend(nested_paths)
                    else:
                        all_matches.append(value)
                        all_paths.append(new_path)

        elif predicate:
            # Handle predicate: /interface[FastEthernet0/0]
            if current_segment in tree and isinstance(tree[current_segment], dict):
                container = tree[current_segment]
                predicate_pattern = predicate.replace("*", ".*")
                for key, value in container.items():
                    if re.match(predicate_pattern, str(key), re.IGNORECASE):
                        new_path = current_path + [current_segment, key]
                        if remaining_segments:
                            if isinstance(value, dict):
                                nested_matches, nested_paths = self._traverse_path_with_tracking(
                                    value, remaining_segments, new_path
                                )
                                all_matches.extend(nested_matches)
                                all_paths.extend(nested_paths)
                        else:
                            all_matches.append(value)
                            all_paths.append(new_path)

        else:
            # Exact match
            if current_segment in tree:
                value = tree[current_segment]
                new_path = current_path + [current_segment]
                if remaining_segments:
                    if isinstance(value, dict):
                        nested_matches, nested_paths = self._traverse_path_with_tracking(
                            value, remaining_segments, new_path
                        )
                        all_matches.extend(nested_matches)
                        all_paths.extend(nested_paths)
                else:
                    all_matches.append(value)
                    all_paths.append(new_path)

        return all_matches, all_paths
