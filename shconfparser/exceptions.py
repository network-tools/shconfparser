"""Custom exception classes for shconfparser.

This module provides domain-specific exceptions for better error handling
and debugging throughout the parsing process.
"""


class ParserError(Exception):
    """Base exception for all parser-related errors."""

    pass


class InvalidDataError(ParserError):
    """Raised when input data is invalid or malformed."""

    pass


class InvalidHeaderError(ParserError):
    """Raised when table header cannot be found or is malformed."""

    def __init__(self, message: str = "Header not found or invalid", pattern: str = ""):
        self.pattern = pattern
        super().__init__(f"{message}: {pattern}" if pattern else message)


class ColumnMismatchError(ParserError):
    """Raised when table columns don't match header columns."""

    def __init__(self, expected: int, found: int):
        self.expected = expected
        self.found = found
        super().__init__(f"Column count mismatch: expected {expected}, found {found}")


class TreeParseError(ParserError):
    """Raised when tree structure parsing fails."""

    pass


class TableParseError(ParserError):
    """Raised when table structure parsing fails."""

    pass


class FileReadError(ParserError):
    """Raised when file reading operations fail."""

    def __init__(self, path: str, reason: str = ""):
        self.path = path
        super().__init__(
            f"Failed to read file '{path}': {reason}" if reason else f"Failed to read file '{path}'"
        )


class SearchError(ParserError):
    """Raised when search operations fail."""

    pass


class ValidationError(ParserError):
    """Raised when data validation fails."""

    pass
