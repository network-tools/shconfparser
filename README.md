# Show Configuration Parser (shconfparser)

[![Build Status](https://travis-ci.org/kirankotari/shconfparser.svg?branch=master)](https://travis-ci.org/kirankotari/shconfparser)
[![GitHub issues open](https://img.shields.io/github/issues/kirankotari/shconfparser.svg?maxAge=2592000)](https://github.com/kirankotari/shconfparser/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage Status](https://coveralls.io/repos/github/kirankotari/shconfparser/badge.svg?branch=master)](https://coveralls.io/github/kirankotari/shconfparser?branch=master)

- [Introduction What is shconfparser](#introduction-what-is-shconfparser)
- [Docs How to use](#docs-how-to-use)
- [Pre-requisites](#pre-requisites)
- [Installation and Downloads](#installation-and-downloads)
- [FAQ](#faq)
- [Other Resources](#other-resources)
- [Bug Tracker and Support](#bug-tracker-and-support)
- [Unit-Tests](#unit-tests)
- [License and Copyright](#license-and-copyright)
- [Author and Thanks](#author-and-thanks)


## Introduction What is shconfparser

Show configuration parser i.e. shconfparser is a Python library, whcih parser Network configurations. 
This library examines the config and breaks it into a set of parent and clild relationships.

shconfparser is a vendor independent library where you can parse the following formats:
 - tree structure *`i.e. show running`*
 - table structure *`i.e. show ip interface`*
 - data structure *`i.e. show version`*

< image: sh run -> format > ... ...

< image: sh ip interface -> format > ... ...

## Docs How to use
....
....

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

Question: ...

Answer: ...

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

 - The current build status is:<br/>[![Build Status](https://travis-ci.org/kirankotari/shconfparser.svg?branch=master)](https://travis-ci.org/kirankotari/shconfparser)

## License and Copyright

 - shconfparser is licensed [MIT](http://opensource.org/licenses/mit-license.php) *2016-2018* <br /> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Author and Thanks

shconfparser was developed by [Kiran Kumar Kotari](https://github.com/kirankotari)


