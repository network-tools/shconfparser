# MODERNIZATION_GUIDE.md

## 🚀 Modernization Guide - shconfparser v3.0

This guide covers the modernization of shconfparser from version 2.x to 3.0 with modern Python tooling.

## What's New in v3.0?

### 1. **Modern Package Management with `uv`**

We've migrated from traditional `setup.py` to modern `pyproject.toml` and adopted `uv` as the recommended package manager.

#### Why uv?
- **10-100x faster** than pip
- Better dependency resolution
- Built-in virtual environment management
- Single tool for all Python package operations

### 2. **Python Version Support**

- ✅ **Supported**: Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- ❌ **Dropped**: Python 2.7, 3.1-3.7

### 3. **Modern Development Tools**

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **uv** | Package manager | `pyproject.toml` |
| **ruff** | Fast linter (replaces flake8) | `pyproject.toml` |
| **black** | Code formatter | `pyproject.toml` |
| **mypy** | Type checker | `pyproject.toml` |
| **pytest** | Testing framework | `pyproject.toml` |
| **pre-commit** | Git hooks | `.pre-commit-config.yaml` |

## Installation

### For Users

#### With pip (traditional):
```bash
pip install shconfparser
```

#### With uv (recommended):
```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install shconfparser
uv pip install shconfparser
```

### For Developers

#### 1. Clone the repository:
```bash
git clone https://github.com/network-tools/shconfparser.git
cd shconfparser
```

#### 2. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 3. Install development dependencies:
```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in editable mode with dev dependencies
uv pip install -e . --dev
```

#### 4. Install pre-commit hooks (optional but recommended):
```bash
uv pip install pre-commit
pre-commit install
```

## Development Workflow

### Using Makefile Commands

We provide a comprehensive Makefile for common tasks:

```bash
# Install the package
make install

# Install with dev dependencies
make dev-install

# Run tests with coverage
make test

# Lint code
make lint

# Format code
make format

# Type check
make type-check

# Run all checks
make check-all

# Clean build artifacts
make clean

# Build distribution packages
make build

# Publish to PyPI
make publish
```

### Manual Commands

#### Running Tests:
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=shconfparser

# Run specific test file
uv run pytest tests/test_parser.py
```

#### Code Quality:
```bash
# Format code
uv run black .

# Lint code
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Type check
uv run mypy shconfparser
```

## Migration from v2.x to v3.0

### For Users

The API remains **backward compatible**. Your existing code will continue to work:

```python
from shconfparser.parser import Parser

p = Parser()
data = p.read('config.txt')
# ... rest of your code
```

### For Contributors

#### Old Way (v2.x):
```bash
# setup.py based
pip install -r requirements_dev.txt
pip install -e .
python setup.py test
```

#### New Way (v3.0):
```bash
# pyproject.toml + uv based
uv pip install -e . --dev
make test
# or
uv run pytest
```

## CI/CD Updates

### GitHub Actions

We now use modern GitHub Actions with uv:

- **Test workflow**: `.github/workflows/test-uv.yml`
  - Tests on Python 3.8-3.13
  - Runs on Ubuntu, macOS, Windows
  - Uploads coverage to Codecov

- **Publish workflow**: `.github/workflows/publish-uv.yml`
  - Builds with uv
  - Publishes to PyPI on release

### Removed:
- Old pytest workflows
- tox.ini (replaced by uv matrix testing)
- requirements*.txt (now in pyproject.toml)
- Pipfile (replaced by uv)

## Project Structure Changes

```
shconfparser/
├── pyproject.toml          # ✨ New: All configuration in one place
├── Makefile                # ✨ New: Easy development commands
├── .pre-commit-config.yaml # ✨ New: Pre-commit hooks
├── .github/workflows/
│   ├── test-uv.yml        # ✨ New: Modern CI with uv
│   └── publish-uv.yml     # ✨ New: Publishing with uv
├── shconfparser/
│   ├── __init__.py        # ✨ Updated: Modern logging, type hints
│   ├── py.typed           # ✨ New: Type information
│   └── ...
├── setup_old.py           # 📦 Archived: Old setup.py
└── ...
```

## Business Standards Compliance

### Code Quality Standards

✅ **Implemented:**
- **PEP 8** compliance via black and ruff
- **Type hints** for better IDE support
- **100% test coverage** target
- **Security scanning** via CodeQL
- **Automated formatting** in CI/CD
- **Pre-commit hooks** for quality gates

### Documentation Standards

✅ **Implemented:**
- Comprehensive README with examples
- API documentation in docstrings
- CHANGELOG for version tracking
- CONTRIBUTING guidelines
- CODE_OF_CONDUCT for community

### Release Process

✅ **Implemented:**
- Semantic versioning (MAJOR.MINOR.PATCH)
- Automated testing before release
- GitHub releases with changelog
- PyPI trusted publishing
- Artifact signing

### Security Standards

✅ **Implemented:**
- CodeQL analysis in CI
- Dependabot for dependency updates
- Security policy (SECURITY.md)
- Regular dependency audits

## Troubleshooting

### uv Installation Issues

**Problem**: `uv: command not found`

**Solution**:
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (if not automatic)
export PATH="$HOME/.cargo/bin:$PATH"
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'shconfparser'`

**Solution**:
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Reinstall in editable mode
uv pip install -e .
```

### Test Failures

**Problem**: Tests fail with import errors

**Solution**:
```bash
# Clean and reinstall
make clean
make dev-install
make test
```

## Resources

- **uv Documentation**: https://docs.astral.sh/uv/
- **ruff Documentation**: https://docs.astral.sh/ruff/
- **Python Packaging Guide**: https://packaging.python.org/
- **pyproject.toml Reference**: https://peps.python.org/pep-0621/

## Support

- Report issues: https://github.com/network-tools/shconfparser/issues
- Ask questions: https://stackoverflow.com (tag: shconfparser)
- Email: kirankotari@live.com

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**Made with ❤️ by the shconfparser team**
