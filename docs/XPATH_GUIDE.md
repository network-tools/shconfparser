# XPath Feature for shconfparser

## Overview

The XPath feature adds powerful querying capabilities to shconfparser, similar to Cisco NSO's XPath search functionality. It allows you to search and navigate through parsed configuration trees using XPath-style query syntax.

## Installation

Already included in shconfparser 3.0.0+

## Quick Start

```python
from shconfparser import Parser

# Parse configuration
p = Parser()
p.read('config.txt')
p.parse_tree()

# Use XPath queries
result = p.xpath('//ip/address')  # Find all IP addresses
print(f"Found {result.count} addresses")
for addr in result.matches:
    print(addr)
```

## Supported XPath Features

### 1. Absolute Paths
Navigate from root with specific path:
```python
result = p.xpath('/interface/GigabitEthernet0-0-1/ip/address')
```

### 2. Recursive Search (`//`)
Find matches anywhere in the tree:
```python
result = p.xpath('//address')  # All addresses at any level
result = p.xpath('//ip/nat')   # All NAT settings under ip
```

### 3. Wildcards (`*`)
Match any key at a level:
```python
# List all interface names
result = p.xpath('/interface/*')

# Get descriptions from all interfaces  
result = p.xpath('/interface/*/description')
```

### 4. Predicates (`[pattern]`)
Filter by pattern with wildcard support:
```python
# Get config for GigabitEthernet interfaces only
result = p.xpath('/interface[GigabitEthernet*]')

# Get IPs from specific interface types
result = p.xpath('/interface[GigabitEthernet*]/ip/address')
```

### 5. Root Path
Get entire tree:
```python
result = p.xpath('/')
```

## XPathResult Object

All queries return an `XPathResult` with:

- `success` (bool): Whether query found matches
- `data` (Any): First match (primary result)
- `matches` (List): All matches found
- `count` (int): Number of matches
- `query` (str): Original query string
- `error` (str|None): Error message if failed

### Boolean Evaluation

```python
result = p.xpath('/hostname')
if result:  # Evaluates to True if success
    print(f"Hostname: {result.data}")
```

## Advanced Usage

### Query Chaining
```python
# Get specific interface first
interface = p.xpath('/interface/GigabitEthernet0-0-1')

# Then query within that interface
nat = p.xpath('/ip/nat', tree=interface.data)
```

### Custom Tree
```python
# Query a custom tree instead of stored one
result = p.xpath('//address', tree=custom_tree)
```

### Pattern Matching
Case-insensitive with wildcard support:
```python
# Matches Loopback0, Loopback1, etc.
result = p.xpath('/interface[Loopback*]')

# Matches anything ending in 0
result = p.xpath('/interface[*0]')
```

## Examples

See `examples/xpath_demo.py` for comprehensive examples.

## Comparison with Cisco NSO

| Feature | Cisco NSO | shconfparser XPath |
|---------|-----------|-------------------|
| Absolute paths | ✓ | ✓ |
| Recursive search | ✓ | ✓ |
| Wildcards | ✓ | ✓ |
| Predicates | ✓ | ✓ (simplified) |
| Attributes | ✓ | - |
| Functions | ✓ | - |
| Axes | ✓ | - |

## Performance

- Efficient for small to medium trees (< 10k nodes)
- Recursive searches scan entire tree
- Use absolute paths when possible for best performance

## Testing

31 comprehensive tests cover all functionality:
```bash
pytest tests/test_xpath.py -v
```

## API Reference

### Parser.xpath()

```python
def xpath(query: str, tree: Optional[TreeData] = None) -> XPathResult:
    """Execute XPath-style query on configuration tree.
    
    Args:
        query: XPath-style query string
        tree: Optional tree to search (uses self.data if not provided)
        
    Returns:
        XPathResult with matches, count, and metadata
    """
```

### XPath Class

```python
from shconfparser.xpath import XPath

xpath = XPath()
result = xpath.query(tree, '//ip/address')
```

## Future Enhancements

Potential additions:
- XPath functions (count(), text(), etc.)
- Attribute filtering `[@attr='value']`
- Multiple predicates
- Parent/ancestor axes
- Index predicates `[1]`, `[last()]`
