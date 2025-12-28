"""shconfparser - Network configuration parser library.

This library parses network device show command outputs and converts them
into structured data formats (tree/table).
"""

import logging
from datetime import datetime
from typing import Optional

# Core exports
from .exceptions import (
    ColumnMismatchError,
    FileReadError,
    InvalidDataError,
    InvalidHeaderError,
    ParserError,
    SearchError,
    TableParseError,
    TreeParseError,
    ValidationError,
)
from .models import (
    FileReadResult,
    ParseResult,
    SearchResult,
    TableData,
    TableParseResult,
    TableRow,
    TreeData,
    TreeParseResult,
    ValidationResult,
)
from .parser import Parser
from .protocols import Parsable, Readable, Searchable, Splittable, Validatable
from .reader import Reader
from .search import Search
from .shsplit import ShowSplit
from .table_parser import TableParser
from .tree_parser import TreeParser

__version__ = "3.0.0"
__author__ = "Kiran Kumar Kotari"
__email__ = "kirankotari@live.com"

__all__ = [
    # Main classes
    "Parser",
    "TreeParser",
    "TableParser",
    "Reader",
    "Search",
    "ShowSplit",
    # Exceptions
    "ParserError",
    "InvalidDataError",
    "InvalidHeaderError",
    "ColumnMismatchError",
    "TreeParseError",
    "TableParseError",
    "FileReadError",
    "SearchError",
    "ValidationError",
    # Models
    "ParseResult",
    "TreeParseResult",
    "TableParseResult",
    "SearchResult",
    "ValidationResult",
    "FileReadResult",
    "TreeData",
    "TableData",
    "TableRow",
    # Protocols
    "Parsable",
    "Readable",
    "Searchable",
    "Splittable",
    "Validatable",
]


# Configure logging
def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """Setup logging configuration.

    Args:
        level: Logging level (default: INFO)
        log_file: Optional log file path
    """
    handlers: list = []

    if log_file:
        file_handler = logging.FileHandler(log_file)
        handlers.append(file_handler)
    else:
        console_handler = logging.StreamHandler()
        handlers.append(console_handler)

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )
    logging.info(f"Logging initialized at {datetime.now()}")


# Initialize default logging
setup_logging()
