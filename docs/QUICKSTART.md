# Quick Start Guide for Contributors

Welcome to shconfparser! This guide will get you up and running in minutes.

## Prerequisites

- Python 3.8 or higher
- Git

## Setup (5 minutes)

### 1. Clone and Navigate
```bash
git clone https://github.com/network-tools/shconfparser.git
cd shconfparser
```

### 2. Install uv (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Setup Development Environment
```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package with dev dependencies
uv pip install -e . --dev
```

### 4. Install Pre-commit Hooks (Optional but Recommended)
```bash
uv pip install pre-commit
pre-commit install
```

## Your First Contribution

### Run Tests
```bash
make test
# or
uv run pytest
```

### Format Code
```bash
make format
# or
uv run black .
```

### Check Code Quality
```bash
make check-all
```

### Make Changes
1. Create a branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run tests: `make test`
4. Format code: `make format`
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Open a Pull Request

## Common Commands

| Command | Description |
|---------|-------------|
| `make dev-install` | Install with dev dependencies |
| `make test` | Run tests with coverage |
| `make lint` | Run linter |
| `make format` | Format code |
| `make type-check` | Run type checker |
| `make check-all` | Run all checks |
| `make clean` | Clean build artifacts |

## Need Help?

- Read [CONTRIBUTING.md](CONTRIBUTING.md)
- Check [MODERNIZATION_GUIDE.md](MODERNIZATION_GUIDE.md)
- Open an [issue](https://github.com/network-tools/shconfparser/issues)

## Pro Tips

1. **Use pre-commit hooks** - They catch issues before you commit
2. **Run `make check-all`** - Before pushing to ensure everything passes
3. **Write tests** - For any new features or bug fixes
4. **Keep it simple** - Small, focused commits are easier to review

Happy coding! 🚀
