# XPath Query Guide

Complete guide for using XPath queries with shconfparser to query network configuration data.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Query Syntax](#query-syntax)
- [Context Options](#context-options)
- [XPathResult Structure](#xpathresult-structure)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Limitations](#limitations)

## Overview

XPath queries provide a powerful way to search and extract data from network configurations parsed in YAML format. Inspired by Cisco NSO, shconfparser's XPath implementation supports hierarchical queries with wildcards, predicates, and context tracking.

### Key Features

- ✅ **Absolute paths** - Direct navigation to specific nodes
- ✅ **Recursive search** - Find patterns anywhere in the tree
- ✅ **Wildcards** - Match multiple similar paths
- ✅ **Predicates** - Handle identifiers with special characters
- ✅ **Context tracking** - Identify match sources in wildcard queries
- ✅ **Path tracking** - Full path to each match

### Requirements

**XPath queries work with modern formats (json or yaml):**

```python
# ✅ Correct - JSON format (hierarchical dict)
p = Parser(output_format='json')
tree = p.parse_tree(data)
result = p.xpath('/hostname')

# ✅ Correct - YAML format (hierarchical dict, same structure as json)
p = Parser(output_format='yaml')
result = p.xpath('/hostname')

# ❌ Wrong - Legacy format not supported
p = Parser()  # Defaults to 'legacy'
result = p.xpath('/hostname')  # Returns error
```

## Quick Start

```python
from shconfparser import Parser

# Initialize parser with modern format (json or yaml)
p = Parser(output_format='json')  # or 'yaml' - both work
data = p.read('running_config.txt')
tree = p.parse_tree(data)

# Simple query
result = p.xpath('/hostname')
print(result.data)  # 'R1'

# Wildcard query with context
result = p.xpath('/interface/*/duplex', context='partial')
for match in result.matches:
    print(match)  # Shows which interface each match came from
```

## Query Syntax

### Absolute Paths

Navigate directly to a specific node:

```python
# Single level
result = p.xpath('/hostname')
# Result: "R1"

# Nested path
result = p.xpath('/interface/FastEthernet0/0/duplex')
# Note: Won't work because "/" in "FastEthernet0/0" splits incorrectly

# Use predicates for identifiers with special characters
result = p.xpath('/interface[FastEthernet0/0]/duplex')
# Result: "auto"

# Deep nesting
result = p.xpath('/interface[FastEthernet0/0]/ip/address')
# Result: "1.1.1.1 255.255.255.0"
```

### Recursive Search (`//`)

Find a key anywhere in the configuration tree:

```python
# Find all occurrences of "duplex"
result = p.xpath('//duplex')
print(result.matches)  # ['auto', 'auto']
print(result.count)    # 2

# Find hostname anywhere
result = p.xpath('//hostname')
# Result: "R1"
```

### Wildcards (`*`)

Match any key at a specific level:

```python
# All interfaces
result = p.xpath('/interface/*')
# Returns: All interface configurations

# Specific attribute across all interfaces
result = p.xpath('/interface/*/duplex')
# Returns: ['auto', 'auto']

# Multiple wildcards
result = p.xpath('/interface/*/ip/*')
# Returns: All IP configuration values
```

### Predicates (`[...]`)

Match specific keys or patterns, especially useful for identifiers with special characters:

```python
# Exact match - handles slashes in interface names
result = p.xpath('/interface[FastEthernet0/0]')
# Returns: FastEthernet0/0 configuration dict

# With continuation path
result = p.xpath('/interface[FastEthernet0/0]/duplex')
# Returns: "auto"

# Predicate with wildcard pattern
result = p.xpath('/interface[FastEthernet*]')
# Returns: All FastEthernet interfaces

result = p.xpath('/interface[FastEthernet*]/duplex')
# Returns: ['auto', 'auto']

# Match pattern
result = p.xpath('/interface[*0/0]')
# Returns: All interfaces ending with "0/0"
```

## Context Options

Context options solve the problem of identifying which match came from where when using wildcards.

### The Problem

```python
result = p.xpath('/interface[FastEthernet*]/ip')
print(result.data)
# {'address': '1.1.1.1 255.255.255.0'}
# ❌ Which FastEthernet interface is this from?
```

### The Solution: Three Context Options

#### 1. `context='none'` (Default)

Returns just the matched values - backward compatible behavior.

```python
result = p.xpath('/interface/*/duplex', context='none')
print(result.matches)
# ['auto', 'auto']
# ❌ Can't tell which interface
```

**Use when:**
- You only care about the values, not the source
- Maintaining backward compatibility
- Processing simple, unambiguous queries

#### 2. `context='partial'` (Recommended)

Shows from the wildcard/predicate match point to the value.

```python
result = p.xpath('/interface/*/duplex', context='partial')
print(result.matches)
# [{'FastEthernet0/0': {'duplex': 'auto'}},
#  {'FastEthernet0/1': {'duplex': 'auto'}}]
# ✅ Can see which interface each match came from
```

**Use when:**
- You need to identify the source of wildcard matches
- You want minimal context (just what's necessary)
- Processing interface-specific or device-specific configs

#### 3. `context='full'`

Shows the complete tree hierarchy from root to value.

```python
result = p.xpath('/interface/*/duplex', context='full')
print(result.matches)
# [{'interface': {'FastEthernet0/0': {'duplex': 'auto'}}},
#  {'interface': {'FastEthernet0/1': {'duplex': 'auto'}}}]
# ✅ Full path context included
```

**Use when:**
- You need complete hierarchical context
- Building configuration diffs or comparisons
- Generating configuration documentation

### Context Comparison

```python
query = '/interface[FastEthernet*]/ip'

# none: Just the IP config
{'address': '1.1.1.1 255.255.255.0'}

# partial: From interface name down
{'FastEthernet0/0': {'ip': {'address': '1.1.1.1 255.255.255.0'}}}

# full: Complete hierarchy
{'interface': {'FastEthernet0/0': {'ip': {'address': '1.1.1.1 255.255.255.0'}}}}
```

## XPathResult Structure

Every XPath query returns an `XPathResult` object:

```python
@dataclass
class XPathResult:
    success: bool               # True if query succeeded
    data: Any                   # First match (primary result)
    matches: List[Any]          # All matches
    count: int                  # Number of matches
    query: str                  # Original query string
    error: Optional[str]        # Error message if failed
    paths: List[List[str]]      # Path components to each match
```

### Field Descriptions

**`success`** - Boolean indicating if query found results
```python
if result:  # or: if result.success:
    print("Found matches!")
```

**`data`** - First match (convenience for single-result queries)
```python
hostname = p.xpath('/hostname').data  # Direct access
```

**`matches`** - List of all matches
```python
for duplex in p.xpath('//duplex').matches:
    print(duplex)
```

**`count`** - Number of matches found
```python
result = p.xpath('/interface/*')
print(f"Found {result.count} interfaces")
```

**`query`** - Original query string (useful for debugging)
```python
print(f"Query: {result.query}")
```

**`error`** - Error message if query failed
```python
if not result.success:
    print(f"Error: {result.error}")
```

**`paths`** - List of path components to each match
```python
result = p.xpath('/interface/*/duplex')
for path in result.paths:
    print(path)
# ['interface', 'FastEthernet0/0', 'duplex']
# ['interface', 'FastEthernet0/1', 'duplex']
```

## Examples

### Example 1: Find All Interface IP Addresses

```python
result = p.xpath('/interface/*/ip/address', context='partial')

for match in result.matches:
    # Each match shows interface name and IP
    interface_name = list(match.keys())[0]
    ip_address = match[interface_name]['ip']['address']
    print(f"{interface_name}: {ip_address}")
# FastEthernet0/0: 1.1.1.1 255.255.255.0
```

### Example 2: Find All Auto-Negotiating Interfaces

```python
result = p.xpath('//duplex', context='partial')

auto_interfaces = []
for match, path in zip(result.matches, result.paths):
    if match == 'auto' or (isinstance(match, dict) and 'auto' in str(match)):
        # path contains: ['interface', 'FastEthernet0/0', 'duplex']
        interface = path[1]
        auto_interfaces.append(interface)

print(f"Auto-negotiating interfaces: {auto_interfaces}")
```

### Example 3: Configuration Validation

```python
# Check if all interfaces have IP addresses
result = p.xpath('/interface/*', context='partial')

for match in result.matches:
    interface_name = list(match.keys())[0]
    interface_config = match[interface_name]
    
    if 'ip' not in interface_config:
        print(f"Warning: {interface_name} has no IP configuration")
    elif 'address' not in interface_config.get('ip', {}):
        print(f"Warning: {interface_name} has no IP address")
```

### Example 4: Bulk Configuration Changes

```python
# Find all interfaces with speed setting
result = p.xpath('/interface/*/speed', context='partial')

changes = []
for match in result.matches:
    interface_name = list(match.keys())[0]
    current_speed = match[interface_name]['speed']
    
    if current_speed != '1000':
        changes.append(f"interface {interface_name}\n speed 1000")

print("Proposed changes:")
print("\n".join(changes))
```

### Example 5: Recursive Search with Filtering

```python
# Find all "auto" settings anywhere in config
result = p.xpath('//auto', context='partial')

# Group by setting type
settings = {}
for match, path in zip(result.matches, result.paths):
    setting_type = path[-1]  # Last element is the setting name
    if setting_type not in settings:
        settings[setting_type] = []
    settings[setting_type].append(path[1] if len(path) > 1 else 'global')

for setting, locations in settings.items():
    print(f"{setting}: {', '.join(locations)}")
```

## Best Practices

### 1. Choose the Right Context

```python
# For simple value extraction
result = p.xpath('/hostname', context='none')

# For identifying wildcard match sources
result = p.xpath('/interface/*/duplex', context='partial')

# For complete hierarchy preservation
result = p.xpath('//important-setting', context='full')
```

### 2. Always Check Success

```python
result = p.xpath('/some/path')
if result.success:
    process_data(result.matches)
else:
    print(f"Query failed: {result.error}")
```

### 3. Use Predicates for Special Characters

```python
# ❌ Wrong - slashes will split incorrectly
result = p.xpath('/interface/FastEthernet0/0/duplex')

# ✅ Correct - use predicates
result = p.xpath('/interface[FastEthernet0/0]/duplex')
```

### 4. Leverage Path Tracking

```python
result = p.xpath('//duplex')
for value, path in zip(result.matches, result.paths):
    full_path = '/'.join(path)
    print(f"{full_path}: {value}")
```

### 5. Combine with Python Processing

```python
# XPath for querying, Python for complex logic
result = p.xpath('/interface/*', context='partial')

for match in result.matches:
    interface = list(match.keys())[0]
    config = match[interface]
    
    # Apply complex business logic
    if needs_update(config):
        generate_config_change(interface, config)
```

## Limitations

### 1. YAML Format Only

```python
# ❌ Won't work with JSON format
p = Parser(output_format='json')
result = p.xpath('/hostname')  # Returns error
```

**Solution:** Use `output_format='json'` or `output_format='yaml'` (modern formats)

### 2. No Attribute Selection

XPath in shconfparser doesn't support attribute selection syntax like `@attribute`.

```python
# ❌ Not supported
result = p.xpath('/interface[@name="FastEthernet0/0"]')

# ✅ Use predicates instead
result = p.xpath('/interface[FastEthernet0/0]')
```

### 3. No Complex Expressions

Boolean logic, arithmetic, and functions are not supported.

```python
# ❌ Not supported
result = p.xpath('/interface[speed > 100]')
result = p.xpath('/interface[duplex="auto" and speed="auto"]')

# ✅ Filter in Python instead
result = p.xpath('/interface/*', context='partial')
filtered = [m for m in result.matches 
            if list(m.values())[0].get('speed') == 'auto']
```

### 4. Case Sensitive

All queries are case-sensitive with case-insensitive matching for wildcards.

```python
result = p.xpath('/Interface')  # Won't match 'interface'
result = p.xpath('/interface[FastEthernet*]')  # Case-insensitive pattern match
```

## Error Handling

```python
# Empty query
result = p.xpath('')
# result.error: "XPath query cannot be empty"

# Invalid query format
result = p.xpath('hostname')  # Missing leading /
# result.error: "XPath query must start with / or //"

# Invalid context
result = p.xpath('/hostname', context='invalid')
# result.error: "Invalid context 'invalid'. Must be 'none', 'partial', or 'full'"

# Legacy format error
p = Parser()  # Defaults to 'legacy'
result = p.xpath('/hostname')
# result.error: "XPath requires modern format (json/yaml)..."
```

## Performance Tips

1. **Use absolute paths** when you know the exact location
   ```python
   # Faster
   result = p.xpath('/interface[FastEthernet0/0]/duplex')
   
   # Slower (searches entire tree)
   result = p.xpath('//duplex')
   ```

2. **Minimize context when possible**
   ```python
   # Lighter processing
   result = p.xpath('/interface/*', context='none')
   
   # More processing for structure building
   result = p.xpath('/interface/*', context='full')
   ```

3. **Use specific predicates over wildcards**
   ```python
   # More specific, faster
   result = p.xpath('/interface[FastEthernet0/0]')
   
   # Less specific, may return more results
   result = p.xpath('/interface[*0/0]')
   ```

---

**For more examples, see:**
- [Main README](../README.md)
- [Quick Start Guide](QUICKSTART.md)
- [Test Suite](../tests/test_xpath.py)

**Need help?** Open an issue on [GitHub](https://github.com/network-tools/shconfparser/issues)
