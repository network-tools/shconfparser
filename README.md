# Show Configuration Parser (shconfparser)

[![Build Status](https://travis-ci.org/kirankotari/shconfparser.svg?branch=master)](https://travis-ci.org/kirankotari/shconfparser)
[![GitHub issues open](https://img.shields.io/github/issues/kirankotari/shconfparser.svg?maxAge=2592000)](https://github.com/kirankotari/shconfparser/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage Status](https://coveralls.io/repos/github/kirankotari/shconfparser/badge.svg?branch=master)](https://coveralls.io/github/kirankotari/shconfparser?branch=master)

- [Introduction](#introduction)
- [Docs](#docs)
- [Pre-requisites](#pre-requisites)
- [Installation and Downloads](#installation-and-downloads)
- [FAQ](#faq)
- [Other Resources](#other-resources)
- [Bug Tracker and Support](#bug-tracker-and-support)
- [Unit-Tests](#unit-tests)
- [License and Copyright](#license-and-copyright)
- [Author and Thanks](#author-and-thanks)

## Introduction

Show configuration parser i.e. shconfparser is a Python library, whcih parser Network configurations. 
This library examines the config and breaks it into a set of parent and clild relationships.

shconfparser is a vendor independent library where you can parse the following formats:

- Tree structure *`i.e. show running`*
- Table structure *`i.e. show ip interface`*
- Data *`i.e. show version`*

[//]: # (TODO: need to add sh run image)
[//]: # (TODO: need to add sh cdp neig image)
[//]: # (TODO: need to add asserts folder)

## Docs

Translating tree structure

```python
>>> from shconfparser.parser import Parser
>>> from os import path
>>> file_path = path.abspath('data/shcommands.txt')
>>> p = Parser()
>>> data = p.read(file_path) # read file content
>>> data = p.split(data) # split each show commands and it's data
>>> data['running'] = p.parse_tree(data['running']) # translating show running data to tree format
>>> p.dump(data['running']) # running data in tree format
```

```json
{"R1#sh run": "None", "Building configuration...": "None", "Current configuration : 891 bytes": "None", "version 12.4": "None", "service timestamps debug datetime msec": "None", "service timestamps log datetime msec": "None", "no service password-encryption": "None", "hostname R1": "None", "boot-start-marker": "None", "boot-end-marker": "None", "no aaa new-model": "None", "memory-size iomem 5": "None", "no ip icmp rate-limit unreachable": "None", "ip cef": "None", "no ip domain lookup": "None", "ip auth-proxy max-nodata-conns 3": "None", "ip admission max-nodata-conns 3": "None", "ip tcp synwait-time 5": "None", "l2vpn": {"bridge group a": {"bridge-domain b": {"interface FastEthernet 0/0": {"static-mac-address test-abc": "None"}}, "bridge-domain c": {"interface FastEthernet 0/1": {"static-mac-address test-xyz": "None"}}}}, "interface FastEthernet0/0": {"ip address 1.1.1.1 255.255.255.0": "None", "duplex auto": "None", "speed auto": "None"}, "interface FastEthernet0/1": {"no ip address": "None", "shutdown": "None", "duplex auto": "None", "speed auto": "None"}, "ip forward-protocol nd": "None", "no ip http server": "None", "no ip http secure-server": "None", "no cdp log mismatch duplex": "None", "control-plane": "None", "line con 0": {"exec-timeout 0 0": "None", "privilege level 15": "None", "logging synchronous": "None"}, "line aux 0": {"exec-timeout 0 0": "None", "privilege level 15": "None", "logging synchronous": "None"}, "line vty 0 4": {"login": "None"}}
```

Translating table structure

```python
>>>  
```

Translating data

```python
>>>  
```

## Pre-requisites

shconfparser supports both trains of **python** `2.7+ and 3.1+`, the OS should not matter.

## Installation and Downloads

The best way to get shconfparser is with setuptools or pip. If you already have setuptools, you can install as usual:

`python -m pip install shconfparser`

Otherwise download it from PyPi, extract it and run the `setup.py` script

`python setup.py install`

If you're Interested in the source, you can always pull from the github repo:

- From github `git clone https://github.com/kirankotari/shconfparser.git`

## FAQ

- **Question:** I want to use shconfparser with Python3, is that safe?  
 **Answer:** As long as you're using python 3.3 or higher, it's safe. I tested every release against python 3.1+, however python 3.1 and 3.2 not running in continuous integration test.  

- **Question:** I want to use shconfparser with Python2, is that safe?  
 **Answer:** As long as you're using python 2.7 or higher, it's safe. I tested against python 2.7.

## Other Resources

- [Python3 documentation](https://docs.python.org/3/) is a good way to learn python
- Python [GeeksforGeeks](https://www.geeksforgeeks.org/python-programming-language/)
- [Ordered Dictionary](https://docs.python.org/2/library/collections.html#collections.OrderedDict)
- [JSON](http://json.org/)

## Bug Tracker and Support

- Please report any suggestions, bug reports, or annoyances with shconfparser through the [Github bug tracker](https://github.com/kirankotari/shconfparser/issues). If you're having problems with general python issues, consider searching for a solution on [Stack Overflow](https://stackoverflow.com/search?q=).
- If you can't find a solution for your problem or need more help, you can [ask a question](https://stackoverflow.com/questions/ask).
- You can also ask on the [Stack Exchange Network Engineering](https://networkengineering.stackexchange.com/) site.

## Unit Tests

- [Travis CI](https://travis-ci.org/kirankotari/shconfparser/builds) project tests shconfparser on Python versions `2.7` through `3.7`.

- The current build status is:  
 [![Build Status](https://travis-ci.org/kirankotari/shconfparser.svg?branch=master)](https://travis-ci.org/kirankotari/shconfparser)

## License and Copyright

- shconfparser is licensed [MIT](http://opensource.org/licenses/mit-license.php) *2016-2018*  
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Author and Thanks

shconfparser was developed by [Kiran Kumar Kotari](https://github.com/kirankotari)
