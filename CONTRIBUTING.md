# Contributing to shconfparser

Thank you for your interest in contributing to shconfparser! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Project Architecture](#project-architecture)
- [Release Process](#release-process)

## 📜 Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** (3.9, 3.10, 3.11, 3.12, 3.13 supported)
- **uv** package manager (recommended) or pip
- **Git** for version control

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/YOUR_USERNAME/shconfparser.git
cd shconfparser
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/network-tools/shconfparser.git
```

## 🛠️ Development Setup

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in editable mode with dev dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks (optional but recommended)
uv run pre-commit install
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Using Makefile

```bash
# Install everything (package + dev tools + pre-commit)
make dev-install
```

## 🔄 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Your Changes

Follow the [Coding Standards](#coding-standards) below.

### 3. Run Tests

```bash
# Run all tests
make test
# or
uv run pytest

# Run with coverage
uv run pytest --cov=shconfparser

# Run specific test file
uv run pytest tests/test_parser.py -v
```

### 4. Run Code Quality Checks

```bash
# Run all checks at once
make check-all

# Or run individually:
make format      # Auto-format with black
make lint        # Check with ruff
make type-check  # Check types with mypy
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature"  # Use conventional commits
```

**Commit Message Format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Build/tooling changes

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📐 Coding Standards

### Style Guide

We follow **PEP 8** with the following tools:

- **Black** (line length: 100) - Code formatting
- **Ruff** - Fast linting
- **MyPy** - Static type checking

### Code Requirements

#### 1. Type Hints

All public functions and methods must have type hints:

```python
def parse_tree(self, lines: List[str]) -> TreeData:
    """Parse hierarchical configuration."""
    ...
```

#### 2. Docstrings

Use Google-style docstrings with full descriptions:

```python
def parse_table(
    self, 
    lines: List[str], 
    headers: List[str]
) -> Optional[TableData]:
    """Parse tabular data into list of dictionaries.
    
    Args:
        lines: Lines containing table data
        headers: List of column header names
        
    Returns:
        List of dictionaries (one per row), or None if header not found
        
    Example:
        >>> parser = Parser()
        >>> table = parser.parse_table(lines, ['Port', 'Status'])
    """
```

#### 3. Error Handling

- Use custom exceptions from `exceptions.py`
- Provide clear error messages with context
- Log errors appropriately

```python
from .exceptions import InvalidHeaderError

try:
    header_index = self._fetch_header(lines, pattern)
except Exception as e:
    raise InvalidHeaderError("Header not found", pattern=pattern)
```

#### 4. Imports

Organize imports in this order:
```python
# Standard library
import json
import logging
from typing import List, Optional

# Third-party (if any)

# Local imports
from .exceptions import ParserError
from .models import TreeData
```

#### 5. Debugging Support

Add `__repr__()` methods to classes:

```python
def __repr__(self) -> str:
    """Return string representation for debugging."""
    return f"Parser(data_keys={len(self.data)}, table_rows={len(self.table)})"
```

### Architecture Guidelines

#### Separation of Concerns

- **Parser**: Orchestrates sub-parsers, maintains backward compatibility
- **TreeParser**: Pure tree parsing logic (stateless)
- **TableParser**: Pure table parsing logic (stateless)
- **Reader**: File I/O operations
- **Search**: Pattern matching utilities
- **ShowSplit**: Command splitting

#### Pure Functions Preferred

Write pure functions where possible:

```python
# Good: Pure function
def parse_tree(self, lines: List[str]) -> TreeData:
    # Takes input, returns output, no side effects
    return self._convert_to_dict(data)

# Avoid: Stateful methods when not needed
def parse_tree(self, lines: List[str]) -> None:
    self.data = self._convert_to_dict(data)  # Side effect
```

#### Protocols for Extensibility

Use protocols for interfaces:

```python
from typing import Protocol

class Parsable(Protocol):
    def parse(self, lines: List[str]) -> Any:
        ...
```

## 🧪 Testing

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names: `test_parse_table_with_missing_header`
- Aim for **80%+ code coverage**

### Test Structure

```python
import pytest
from shconfparser import Parser

class TestParser:
    @pytest.fixture
    def parser(self):
        return Parser()
    
    def test_parse_tree_valid_input(self, parser):
        """Test tree parsing with valid hierarchical input."""
        lines = ['interface Ethernet0', '  ip address 1.1.1.1']
        result = parser.parse_tree(lines)
        assert 'interface Ethernet0' in result
        assert result['interface Ethernet0'] is not None
```

### Running Tests

```bash
# All tests
make test

# Specific test
uv run pytest tests/test_parser.py::TestParser::test_tree_parser -v

# With coverage report
uv run pytest --cov=shconfparser --cov-report=html

# Fast fail (stop on first failure)
uv run pytest -x
```

### Test Coverage

Check coverage:
```bash
make test
# Coverage report generated in htmlcov/
open htmlcov/index.html
```

## 📚 Documentation

### Docstring Requirements

All public APIs must have docstrings with:
- Brief description
- Args section
- Returns section
- Raises section (if applicable)
- Example section (recommended)

### Updating Documentation

If you add/change features, update:
- Docstrings in code
- README.md (if user-facing)
- CHANGELOG.md (add to Unreleased section)
- docs/ files (if major change)

## 🔀 Pull Request Process

### Before Submitting

✅ **Checklist:**
- [ ] Tests pass (`make test`)
- [ ] Code formatted (`make format`)
- [ ] Linting passes (`make lint`)
- [ ] Type checking passes (`make type-check`)
- [ ] All checks pass (`make check-all`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (in Unreleased section)
- [ ] Commit messages follow conventional commits format

### PR Title Format

Use conventional commit format:
- `feat: Add TreeParser class for better separation of concerns`
- `fix: Handle mixed indentation in tree parsing`
- `docs: Update contributing guidelines`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- Describe tests added/modified
- Mention if manual testing was done

## Checklist
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG updated
```

### Review Process

1. **Automated Checks**: CI will run tests on multiple Python versions (3.9-3.13) and OSes
2. **Code Review**: Maintainer will review your code
3. **Feedback**: Address review comments
4. **Approval**: Once approved, maintainer will merge

## 🏗️ Project Architecture

### Module Structure

```
shconfparser/
├── __init__.py           # Public API exports
├── exceptions.py         # Custom exception classes
├── models.py             # Dataclasses for structured results
├── protocols.py          # Interface definitions
├── parser.py             # Main Parser orchestrator
├── tree_parser.py        # Tree structure parsing
├── table_parser.py       # Table structure parsing
├── reader.py             # File I/O operations
├── search.py             # Pattern search utilities
└── shsplit.py            # Command splitter
```

### Key Design Principles

1. **Separation of Concerns**: Each module has single responsibility
2. **Pure Functions**: Stateless parsing where possible
3. **Backward Compatibility**: Old APIs still work
4. **Type Safety**: Full type hints with mypy validation
5. **Error Context**: Rich exceptions with metadata
6. **Extensibility**: Protocol-based interfaces

### Adding New Features

When adding features:
1. Consider which module is responsible
2. Add to appropriate parser (Tree/Table/etc.)
3. Update main Parser if needed for orchestration
4. Add custom exception if needed
5. Create dataclass model for structured results (optional)
6. Write comprehensive tests
7. Document thoroughly

## 🚢 Release Process

Releases are managed by maintainers:

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create release tag: `git tag v3.0.1`
4. Push tag: `git push --tags`
5. GitHub Actions will automatically publish to PyPI

## 💡 Getting Help

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Email**: kirankotari@live.com

## 🙏 Thank You!

Your contributions make shconfparser better for everyone. We appreciate your time and effort!

---

**Quick Links:**
- [README](README.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [License](LICENSE)
- [Changelog](CHANGELOG.md)
