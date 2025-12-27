"""Reader module for file operations.

This module provides the Reader class for reading configuration files.
"""

import builtins
import logging
from os import path
from typing import List, Optional

from .exceptions import FileReadError

logger = logging.getLogger(__name__)


class Reader:
    """File reader for network configuration files.

    Attributes:
        path: File path to read
        data: File contents as list of lines
        encoding: File encoding (default: utf-8)
    """

    def __init__(self, file_path: str, encoding: str = "utf-8") -> None:
        """Initialize the Reader.

        Args:
            file_path: Path to file to read
            encoding: File encoding (default: utf-8)

        Raises:
            FileReadError: If file cannot be read
        """
        if not file_path or not isinstance(file_path, str):
            raise FileReadError(str(file_path), "Invalid file path")

        self.path: str = file_path
        self.encoding: str = encoding
        self.data: Optional[List[str]] = self.read()

    def __repr__(self) -> str:
        """Return string representation for debugging."""
        return f"Reader(path='{self.path}', lines={len(self.data) if self.data else 0})"

    def _isfile(self) -> bool:
        """Check if path exists and is a file.

        Returns:
            True if path is a valid file, False otherwise
        """
        if path.exists(self.path):
            return path.isfile(self.path)
        return False

    def read(self) -> Optional[List[str]]:
        """Read file contents with robust error handling.

        Returns:
            List of lines from file, or None if file doesn't exist

        Raises:
            FileReadError: If file read fails for reasons other than file not found
        """
        if not self._isfile():
            logger.warning(f"File not found or not accessible: {self.path}")
            return None

        try:
            with builtins.open(self.path, encoding=self.encoding) as f:
                lines = f.readlines()
                logger.debug(f"Successfully read {len(lines)} lines from {self.path}")
                return lines
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error reading {self.path}: {e}")
            raise FileReadError(self.path, f"Encoding error: {e}")
        except PermissionError as e:
            logger.error(f"Permission denied reading {self.path}: {e}")
            raise FileReadError(self.path, "Permission denied")
        except Exception as e:
            logger.error(f"Unexpected error reading {self.path}: {e}")
            raise FileReadError(self.path, str(e))
