# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-12-27

### 🎉 Major Release - Modernization

This is a major release focused on modernizing the project infrastructure and tooling while maintaining API backward compatibility.

### Added
- ✨ **pyproject.toml** - Modern Python packaging configuration
- ✨ **uv support** - Fast, modern package manager integration
- ✨ **ruff** - Fast Python linter (replaces flake8)
- ✨ **black** - Code formatter for consistent style
- ✨ **mypy** - Static type checker
- ✨ **pre-commit hooks** - Automated code quality checks
- ✨ **Makefile** - Convenient development commands
- ✨ **Type hints** - Improved IDE support and type safety
- ✨ **py.typed** marker - PEP 561 compliance
- ✨ **Modern CI/CD** - GitHub Actions with uv
- ✨ **MODERNIZATION_GUIDE.md** - Comprehensive migration guide
- ✨ **BUSINESS_STANDARDS.md** - Enterprise compliance documentation
- ✨ **PYTHON_COMPATIBILITY.md** - Version support documentation

### Changed
- 🔄 **Python version support** - Now requires Python 3.8+ (dropped 2.7, 3.1-3.7)
- 🔄 **Packaging** - Migrated from setup.py to pyproject.toml
- 🔄 **Build backend** - Now uses hatchling
- 🔄 **Logging** - Modernized with better defaults and configuration
- 🔄 **Development workflow** - Simplified with uv and Makefile
- 🔄 **CI/CD** - Updated to use modern GitHub Actions with uv
- 🔄 **Documentation** - Enhanced README with modern installation instructions
- 🔄 **Code quality** - Automated formatting and linting

### Deprecated
- ⚠️ **Python 2.7** - No longer supported (use version 2.2.5 for Python 2.7)
- ⚠️ **Python 3.1-3.7** - No longer supported
- ⚠️ **setup.py** - Replaced by pyproject.toml (archived as setup_old.py)
- ⚠️ **tox.ini** - Replaced by uv matrix testing
- ⚠️ **requirements*.txt** - Dependencies now in pyproject.toml
- ⚠️ **Pipfile** - Replaced by uv

### Removed
- ❌ Support for Python versions < 3.8

### Fixed
- 🐛 Improved error handling in logging setup
- 🐛 Better type safety across the codebase

### Security
- 🔒 Added CodeQL security scanning
- 🔒 Dependency security auditing
- 🔒 Pre-commit security checks

### Migration Notes
- **For Users**: API is fully backward compatible. Just upgrade: `pip install --upgrade shconfparser`
- **For Developers**: See [MODERNIZATION_GUIDE.md](MODERNIZATION_GUIDE.md) for complete migration instructions
- **Python 2.7 Users**: Stay on version 2.2.5: `pip install shconfparser==2.2.5`

---

## [2.2.5] - 2021-07-XX

### Added
- Added #25 Feature: Adding GitHub actions
- Added #23 Create codeql-analysis.yml
- Added pytest for 3.x and 2.7.x
- Added GitHub action to upload package to PyPI

### Changed
- Moved from travis to GitHub Actions
- Moved from coveralls to codecov.io

### Fixed
- Updated #22 Bump urllib3 from 1.26.4 to 1.26.5
