# Documentation

Welcome to the shconfparser documentation!

## 📚 Documentation Index

### Getting Started

| Document | Description | Audience |
|----------|-------------|----------|
| [Quick Start](QUICKSTART.md) | 5-minute contributor setup guide | New contributors |

### Detailed Guides

| Document | Description | Audience |
|----------|-------------|----------|
| [Modernization Guide](MODERNIZATION_GUIDE.md) | Complete v2.x to v3.0 migration guide | Existing users, developers |
| [Architecture](ARCHITECTURE.md) | Visual architecture diagrams and structure | Developers, architects |
| [Business Standards](BUSINESS_STANDARDS.md) | Enterprise compliance documentation | Maintainers, enterprises |
| [Python Compatibility](PYTHON_COMPATIBILITY.md) | Python version support details | All users |

### Reference

| Document | Description | Audience |
|----------|-------------|----------|
| [Modernization Summary](MODERNIZATION_SUMMARY.md) | Detailed summary of all changes | Maintainers, contributors |

## 🚀 Quick Links

### For New Users
1. Start with the main [README.md](../README.md)
2. Follow [Installation instructions](../README.md#installation-and-downloads)
3. Check [Usage Examples](../README.md#usage-examples)

### For Contributors
1. Read [QUICKSTART.md](QUICKSTART.md) (5 minutes)
2. Review [Architecture](ARCHITECTURE.md)
3. See main [CONTRIBUTING.md](../CONTRIBUTING.md)

### For Maintainers
1. Check [Business Standards](BUSINESS_STANDARDS.md) for compliance
2. Read [Modernization Summary](MODERNIZATION_SUMMARY.md) for details

## 📖 Document Descriptions

### QUICKSTART.md
Fast track to getting set up as a contributor. Covers environment setup, common commands, and first contribution steps.

### MODERNIZATION_GUIDE.md
Comprehensive guide covering:
- What's new in v3.0
- Installation methods (pip & uv)
- Development workflow
- Migration from v2.x
- CI/CD updates
- Troubleshooting

### BUSINESS_STANDARDS.md
Enterprise-grade compliance documentation covering:
- Code quality standards (PEP 8, type hints)
- Security standards (CodeQL, Dependabot)
- Documentation standards
- Testing standards (80%+ coverage)
- Release management (SemVer)
- Dependency management
- Licensing and legal
- Community and support

### ARCHITECTURE.md
Visual diagrams and explanations of:
- Before/after comparison
- Development workflow
- Package structure
- Tool ecosystem
- Testing matrix
- Release pipeline
- Benefits by stakeholder

### PYTHON_COMPATIBILITY.md
Python version support information:
- Current support: Python 3.8-3.13
- Migration instructions

### MODERNIZATION_SUMMARY.md
Detailed summary of the modernization project:
- Overview of changes
- Before/after comparisons
- Files created/modified
- Benefits achieved
- Testing instructions
- Success metrics

## 🔍 Finding Information

### I want to...

- **Get started contributing** → [QUICKSTART.md](QUICKSTART.md)
- **Understand v3.0 changes** → [MODERNIZATION_GUIDE.md](MODERNIZATION_GUIDE.md)
- **Migrate from v2.x** → [MODERNIZATION_GUIDE.md](MODERNIZATION_GUIDE.md#migration-from-v2x-to-v30)
- **Learn about the architecture** → [ARCHITECTURE.md](ARCHITECTURE.md)
- **Check compliance** → [BUSINESS_STANDARDS.md](BUSINESS_STANDARDS.md)
- **Understand Python support** → [PYTHON_COMPATIBILITY.md](PYTHON_COMPATIBILITY.md)

## 🛠️ Development Quick Reference

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e . --dev

# Common tasks
make test          # Run tests
make format        # Format code
make lint          # Lint code
make check-all     # Run all checks
```

See [QUICKSTART.md](QUICKSTART.md) for more details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/network-tools/shconfparser/issues)
- **Questions**: [Stack Overflow](https://stackoverflow.com) (tag: shconfparser)
- **Email**: kirankotari@live.com

## 📄 License

All documentation is part of the shconfparser project and is licensed under the MIT License.

---

**Last Updated**: December 27, 2025  
**Version**: 3.0.0
