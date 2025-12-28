"""Data models for shconfparser.

This module provides dataclasses for structured return types,
improving type safety and code clarity.
"""

from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

# Type aliases for complex structures
TreeData = OrderedDict[str, Union[str, "TreeData"]]
TableRow = Dict[str, str]
TableData = List[TableRow]


@dataclass
class ParseResult:
    """Result of a parsing operation.

    Attributes:
        success: Whether parsing succeeded
        data: Parsed data structure
        error: Error message if parsing failed
        warnings: List of warning messages
    """

    success: bool
    data: Any = None
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        """Allow boolean evaluation of result."""
        return self.success


@dataclass
class TreeParseResult(ParseResult):
    """Result of tree parsing operation.

    Attributes:
        success: Whether parsing succeeded
        data: Parsed tree structure (OrderedDict)
        error: Error message if parsing failed
        warnings: List of warning messages
        depth: Maximum depth of parsed tree
    """

    data: Optional[TreeData] = None
    depth: int = 0


@dataclass
class TableParseResult(ParseResult):
    """Result of table parsing operation.

    Attributes:
        success: Whether parsing succeeded
        data: Parsed table data (List of dicts)
        error: Error message if parsing failed
        warnings: List of warning messages
        row_count: Number of rows parsed
        column_count: Number of columns in table
        headers: List of column headers
    """

    data: Optional[TableData] = None
    row_count: int = 0
    column_count: int = 0
    headers: List[str] = field(default_factory=list)


@dataclass
class SearchResult:
    """Result of a search operation.

    Attributes:
        found: Whether match was found
        match: The matched object
        key: The key where match was found (for tree searches)
        row_index: Row index where match was found (for table searches)
    """

    found: bool
    match: Any = None
    key: Optional[str] = None
    row_index: Optional[int] = None

    def __bool__(self) -> bool:
        """Allow boolean evaluation of result."""
        return self.found


@dataclass
class ValidationResult:
    """Result of data validation.

    Attributes:
        valid: Whether data is valid
        errors: List of validation error messages
        warnings: List of validation warnings
    """

    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        """Allow boolean evaluation of result."""
        return self.valid


@dataclass
class FileReadResult:
    """Result of file reading operation.

    Attributes:
        success: Whether file was read successfully
        lines: List of lines read from file
        path: Path to the file
        error: Error message if reading failed
        encoding: File encoding used
    """

    success: bool
    lines: Optional[List[str]] = None
    path: str = ""
    error: Optional[str] = None
    encoding: str = "utf-8"

    def __bool__(self) -> bool:
        """Allow boolean evaluation of result."""
        return self.success
