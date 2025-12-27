"""Table parser for structured table data.

This module provides the TableParser class for parsing table-formatted
output (with headers and rows) into list of dictionaries.
"""

import logging
import re
from typing import Dict, List, Optional

from .exceptions import ColumnMismatchError, InvalidHeaderError, TableParseError, ValidationError
from .models import TableData, TableParseResult

logger = logging.getLogger(__name__)


class TableParser:
    """Parser for table-structured data.

    This class handles parsing of tabular data with headers and rows
    into lists of dictionaries, where each dict represents a row.
    """

    def __init__(self) -> None:
        """Initialize the TableParser."""
        self.header_pattern: str = ""
        self.header_names: List[str] = []
        self.column_indexes: List[int] = []

    def __repr__(self) -> str:
        """Return string representation for debugging."""
        return f"TableParser(headers={len(self.header_names)})"

    def _fetch_header(self, lines: List[str], pattern: str) -> int:
        """Find the header line index in a table.

        Args:
            lines: List of text lines
            pattern: Regex pattern to match header

        Returns:
            Index of header line

        Raises:
            InvalidHeaderError: If header not found
        """
        compiled_pattern = re.compile(pattern)
        for i, line in enumerate(lines):
            result = compiled_pattern.match(line)
            if result:
                return i
        raise InvalidHeaderError("Header not found", pattern=pattern)

    def _fetch_column_position(self, header: str, header_names: List[str]) -> List[int]:
        """Determine column positions from header line.

        Args:
            header: Header line string
            header_names: List of expected column names

        Returns:
            List of column start positions
        """
        position: List[int] = []
        for header_name in header_names:
            pos = header.find(header_name)
            if pos == -1:
                logger.warning(f"Header '{header_name}' not found in line")
            position.append(pos)
        return position

    def _fetch_table_column(
        self, line: str, start: int, end: int, key: str, data: Dict[str, str]
    ) -> None:
        """Extract column data from a table row.

        Args:
            line: Row text
            start: Column start position
            end: Column end position
            key: Column header name
            data: Dictionary to populate with column data
        """
        col_data = str(line[start:end]).strip()
        if col_data:
            data[key] = col_data

    def _fetch_table_row(
        self,
        line: str,
        data: Dict[str, str],
        table: List[Dict[str, str]],
        column_indexes: List[int],
        header_names: List[str],
    ) -> Dict[str, str]:
        """Parse a single table row.

        Args:
            line: Row text
            data: Current row data dictionary
            table: Table to append completed row to
            column_indexes: Column start positions
            header_names: Column header names

        Returns:
            Empty dictionary for next row
        """
        if len(line) < column_indexes[-1]:
            data[header_names[0]] = line.strip()
            return data

        for i, column_index in enumerate(column_indexes):
            try:
                start, end = column_index, column_indexes[i + 1]
                self._fetch_table_column(line, start, end, header_names[i], data)
            except IndexError:
                continue

        self._fetch_table_column(
            line, start=column_indexes[-1], end=len(line), key=header_names[-1], data=data
        )
        table.append(data)
        return {}

    def _fetch_table_data(
        self,
        lines: List[str],
        header_index: int,
        pattern: str,
        column_indexes: List[int],
        header_names: List[str],
    ) -> TableData:
        """Extract all table rows from lines.

        Args:
            lines: All text lines
            header_index: Index where header was found
            pattern: Pattern to identify end of table
            column_indexes: Column start positions
            header_names: Column header names

        Returns:
            List of dictionaries representing table rows
        """
        table: TableData = []
        data: Dict[str, str] = {}

        for i in range(header_index + 1, len(lines)):
            if pattern in lines[i] or len(lines[i]) < 2:
                break
            if "---" in lines[i] or "===" in lines[i]:
                continue
            data = self._fetch_table_row(lines[i], data, table, column_indexes, header_names)

        return table

    def _convert(self, lst: List[str], re_escape: bool) -> List[str]:
        """Convert list of strings to regex patterns.

        Args:
            lst: List of strings to convert
            re_escape: Whether to escape regex special characters

        Returns:
            List of regex pattern strings
        """
        lst1: List[str] = []
        for each in lst:
            if re_escape:
                lst1.append(re.escape(each))
            else:
                lst1.append(each.replace(" ", r"\s+"))
        return lst1

    def parse_table(
        self,
        lines: List[str],
        header_keys: List[str],
        pattern: str = "",
        re_split: bool = False,
        custom_pattern: Optional[str] = None,
    ) -> TableData:
        """Parse table structure with headers and rows.

        This is a pure function that takes lines and returns table data
        without maintaining state.

        Args:
            lines: Input lines containing table data
            header_keys: Expected header column names
            pattern: Pattern to identify end of table (default: empty)
            re_split: Whether to use regex splitting (default: False)
            custom_pattern: Custom header pattern (overrides building from header_keys)

        Returns:
            List of dictionaries representing table rows

        Raises:
            TableParseError: If parsing fails
            ValidationError: If input data is invalid
            InvalidHeaderError: If header cannot be found
            ColumnMismatchError: If columns don't match

        Example:
            >>> parser = TableParser()
            >>> lines = ['Port  Status', 'Gi0/1 up', 'Gi0/2 down']
            >>> table = parser.parse_table(lines, ['Port', 'Status'])
        """
        if not lines:
            raise ValidationError("Input lines cannot be empty")

        if not header_keys:
            raise ValidationError("Header keys cannot be empty")

        if not isinstance(lines, list):
            raise ValidationError(f"Expected list, got {type(lines)}")

        try:
            # Build or use custom header pattern
            if custom_pattern:
                header_pattern = custom_pattern
            else:
                header_names = self._convert(header_keys, re_split)
                header_pattern = "".join(header_names)

            # Find header
            header_index = self._fetch_header(lines, header_pattern)

            # Get column positions
            column_indexes = self._fetch_column_position(lines[header_index], header_keys)

            # Parse table data
            table = self._fetch_table_data(
                lines, header_index, pattern, column_indexes, header_keys
            )

            return table

        except (InvalidHeaderError, ColumnMismatchError):
            raise
        except Exception as e:
            if isinstance(e, (TableParseError, ValidationError)):
                raise
            raise TableParseError(f"Failed to parse table structure: {str(e)}") from e

    def parse_table_safe(
        self,
        lines: List[str],
        header_keys: List[str],
        pattern: str = "",
        re_split: bool = False,
        custom_pattern: Optional[str] = None,
    ) -> TableParseResult:
        """Parse table structure with structured result.

        This method wraps parse_table() to return a structured result
        instead of raising exceptions.

        Args:
            lines: Input lines containing table data
            header_keys: Expected header column names
            pattern: Pattern to identify end of table
            re_split: Whether to use regex splitting
            custom_pattern: Custom header pattern

        Returns:
            TableParseResult with success status and data or error
        """
        try:
            table = self.parse_table(lines, header_keys, pattern, re_split, custom_pattern)
            return TableParseResult(
                success=True,
                data=table,
                row_count=len(table),
                column_count=len(header_keys),
                headers=header_keys,
            )
        except ValidationError as e:
            return TableParseResult(success=False, error=f"Validation error: {str(e)}")
        except InvalidHeaderError as e:
            return TableParseResult(success=False, error=str(e))
        except ColumnMismatchError as e:
            return TableParseResult(success=False, error=str(e))
        except TableParseError as e:
            return TableParseResult(success=False, error=str(e))
        except Exception as e:
            logger.exception("Unexpected error during table parsing")
            return TableParseResult(success=False, error=f"Unexpected error: {str(e)}")
