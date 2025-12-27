# Show Configuration Parser (shconfparser)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/network-tools/shconfparser/actions/workflows/test-uv.yml/badge.svg)](https://github.com/network-tools/shconfparser/actions/workflows/test-uv.yml)
[![codecov](https://codecov.io/gh/network-tools/shconfparser/branch/master/graph/badge.svg?token=3HcQhmQJnL)](https://codecov.io/gh/network-tools/shconfparser)
[![Downloads](https://pepy.tech/badge/shconfparser)](https://pepy.tech/project/shconfparser)
[![GitHub issues open](https://img.shields.io/github/issues/network-tools/shconfparser.svg?)](https://github.com/network-tools/shconfparser/issues)
[![CodeQL](https://github.com/network-tools/shconfparser/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/network-tools/shconfparser/actions/workflows/codeql-analysis.yml)
[![PyPI](https://github.com/network-tools/shconfparser/actions/workflows/publish-uv.yml/badge.svg)](https://github.com/network-tools/shconfparser/actions/workflows/publish-uv.yml)

> 🚀 **Version 3.0** - Modern Python library (3.8+) with uv support! See [docs/](docs/) for guides.

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Support](#support)
- [License](#license)

## Introduction

Show configuration parser (shconfparser) is a Python library for parsing network device configurations. 
This library examines the config and breaks it into a set of parent and clild relationships.

shconfparser is a vendor independent library where you can parse the following formats:

- Tree structure *`i.e. show running`*
- Table structure *`i.e. show ip interface`*
- Data *`i.e. show version`*

Tree Structure

![show run to tree structure](https://raw.githubusercontent.com/kirankotari/shconfparser/master/asserts/img/sh_run.png)

Table Structure

![show cdp neighbour to table structure](https://raw.githubusercontent.com/kirankotari/shconfparser/master/asserts/img/sh_cdp_neighbor.png)

## Key Features

✨ **Zero Dependencies** - Uses only Python standard library  
⚡ **Fast** - Modern tooling with uv package manager support  
🔒 **Type Safe** - Full type hints and py.typed marker  
🎯 **Vendor Independent** - Works with any network device configuration  
📊 **Multiple Formats** - Parse trees, tables, and unstructured data  
🧪 **Well Tested** - 80%+ code coverage, tested on Python 3.8-3.13  

## Quick Start

### Installation

```bash
pip install shconfparser
```

**Faster with uv:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install shconfparser
```

### Basic Usage

**Single show command:**
```python
from shconfparser.parser import Parser

p = Parser()
data = p.read('running_config.txt')

# Parse directly (no split needed for single show running command)
tree = p.parse_tree(data)
print(p.dump(tree, indent=2))
```

<details>
<summary>Alternative: Access internal properties</summary>

```python
p = Parser()
p.read('running_config.txt')

# Access reader data directly
tree = p.parse_tree(p.r.data)
print(p.dump(tree, indent=4))
```
</details>

**Multiple show commands in one file:**
```python
from shconfparser.parser import Parser

p = Parser()
data = p.read('multiple_commands.txt')  # Contains multiple show outputs
data = p.split(data)  # Split into separate commands
data.keys()
# odict_keys(['running', 'version', 'cdp_neighbors', 'ip_interface_brief'])

# Now parse each command separately
data['running'] = p.parse_tree(data['running'])

headers = ['Device ID', 'Local Intrfce', 'Holdtme', 'Capability', 'Platform', 'Port ID']
data['cdp_neighbors'] = p.parse_table(data['cdp_neighbors'], header_names=headers)

print(p.dump(data['running'], indent=2))
```

<details>
<summary>Alternative: Access internal properties</summary>

```python
p = Parser()
p.read('multiple_commands.txt')
p.split(p.r.data)

# Access split data from internal property
data = p.s.shcmd_dict
data['running'] = p.parse_tree(data['running'])
print(p.dump(data['running'], indent=4))
```
</details>

## Usage Examples

### Check Library Version

```python
import shconfparser
print(shconfparser.__version__)  # '3.0.0'
```

### Parse Tree Structure (show running-config)

```python
from shconfparser.parser import Parser

p = Parser()

# Single command file - parse directly
data = p.read('running_config.txt')
tree = p.parse_tree(data)  # No split() needed

# Access nested configuration
print(p.dump(tree['interface FastEthernet0/0'], indent=2))
# {
#   "ip address 1.1.1.1 255.255.255.0": null,
#   "duplex auto": null,
#   "speed auto": null
# }
```

### Parse Table Structure (show cdp neighbors)

```python
# Single command file
p = Parser()
data = p.read('cdp_neighbors.txt')

# Parse table directly (no split needed)
headers = ['Device ID', 'Local Intrfce', 'Holdtme', 'Capability', 'Platform', 'Port ID']
cdp_data = p.parse_table(data, header_names=headers)

# Access as list of dictionaries
for neighbor in cdp_data:
    print(f"{neighbor['Device ID']} on {neighbor['Local Intrfce']}")
# Output: R2 on Fas 0/0
```

### Parse Unstructured Data (show version)

```python
# Single command file
p = Parser()
data = p.read('show_version.txt')

# Parse show version output directly
version_data = p.parse_data(data)  # No split() needed

# Search for specific information
import re
for line in version_data.keys():
    if re.search(r'IOS.*Version', line):
        print(line)
# Output: Cisco IOS Software, 3700 Software (C3725-ADVENTERPRISEK9-M), Version 12.4(25d)...
```

### Search in Tree

```python
# Search for all interfaces
pattern = r'interface\s+\w+.*'
matches = p.search.search_all_in_tree(pattern, tree)

for key, value in matches.items():
    print(value)
# interface FastEthernet0/0
# interface FastEthernet0/1
```

### Search in Table

```python
# Find specific device in CDP table
pattern = r'R\d+'
match = p.search.search_in_table(pattern, cdp_data, 'Device ID')
print(match)
# {'Device ID': 'R2', 'Local Intrfce': 'Fas 0/0', ...}
```

### Alternative: Using Individual Components

<details>
<summary>For advanced users who need granular control</summary>

```python
from shconfparser import Reader, ShowSplit, TreeParser, TableParser

# For multiple show commands
reader = Reader('multiple_commands.txt')
splitter = ShowSplit()
data = splitter.split(reader.data)  # Split only if multiple commands

# Use specific parsers
tree_parser = TreeParser()
table_parser = TableParser()

running = tree_parser.parse(data['running'])
cdp = table_parser.parse(data['cdp_neighbors'], header_names=headers)
```
</details>

**💡 Remember:** Use `split()` only when your file contains **multiple** show commands. For single command files, parse directly.

**📖 For more examples, see [docs/](docs/) folder.**

## Documentation

📚 **Complete documentation**: [docs/README.md](docs/README.md)

### For Users

| Guide | Description |
|-------|-------------|
| [Usage Examples](docs/EXAMPLES.md) | Detailed parsing examples (tree, table, data) |
| [API Reference](docs/API.md) | Complete API documentation |
| [Migration Guide](docs/MODERNIZATION_GUIDE.md) | Upgrade from v2.x to v3.0 |
| [Python Compatibility](docs/PYTHON_COMPATIBILITY.md) | Python version support |

### For Contributors

| Guide | Description |
|-------|-------------|
| [Quick Start](docs/QUICKSTART.md) | 5-minute contributor setup |
| [Contributing Guide](CONTRIBUTING.md) | How to contribute |
| [Architecture](docs/ARCHITECTURE.md) | System design and structure |
| [Business Standards](docs/BUSINESS_STANDARDS.md) | Quality and compliance standards |

## Support

### Getting Help

- 📖 **Documentation**: [docs/README.md](docs/README.md)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/network-tools/shconfparser/issues)
- 💬 **Questions**: [Stack Overflow](https://stackoverflow.com) (tag: `shconfparser`)
- 📧 **Email**: kirankotari@live.com

### Frequently Asked Questions

**Q: What Python versions are supported?**  
A: Python 3.8-3.13 are fully tested and supported.

**Q: Does this work with my network vendor?**  
A: Yes! shconfparser is vendor-independent and works with any hierarchical configuration format.

**Q: Are there any dependencies?**  
A: No runtime dependencies - uses only Python standard library.

**Q: How do I migrate from v2.x?**  
A: The API is backward compatible. Just run `pip install --upgrade shconfparser`. See [Migration Guide](docs/MODERNIZATION_GUIDE.md) for details.

### Community

- 🌟 **Star us** on [GitHub](https://github.com/network-tools/shconfparser)
- 🤝 **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- 📊 **CI/CD**: Automated testing on Python 3.8-3.13 across Ubuntu, macOS, Windows

## License

MIT License © 2016-2025 [Kiran Kumar Kotari](https://github.com/kirankotari)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Special thanks to all [contributors](https://github.com/network-tools/shconfparser/graphs/contributors)
