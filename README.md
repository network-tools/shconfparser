Introduction: What is shconfparser?
Docs
Pre-requisites
Installation and Downloads
FAQ
Other Resources
Bug Tracker and Support
Unit-Tests
License and Copyright
Author and Thanks

Introduction: What is shconfparser?

shconfparser is a Python library, whcih parser through Network configurations. 
The library examines the config and breaks it into a set of parent and clild relationships.

shconfparser is a vendor independent library where you can parse the following formats:
    - tree structure i.e. show running
    - table structure i.e. show ip interface
    - data structure i.e. show version

< image: sh run -> format >
< image: sh ip interface -> format >


Docs

....

Pre-requisites

shconfparser supports both trains of python i.e. 2.7+ and 3.1+;
the OS should not matter.

Installation and Downloads

The best way to get shconfparser is with setuptools or pip. If you already 
have setuptools, you can install as usual: 

< code: python -m pip install shconfparser >

Otherwise download it from PyPi, extract it and run the setup.py script

< code: python setup.py install >

If you're Interested in the source, you can always pull from the github repo:
. From github:
    git clone https://url.git

FAQ

1. Question: ...
Answer: ...

...
upto 5

Other Resources
...

Bug Tracker and Support

. Please report any suggestions, bug reports, or annoyances with shconfparser through the github bug tracker.
. If you're having problems with general python issues, consider searching for a solution on Stack Overflow. 
If you can't find a solution for your problem or need more help, you can ask a question.
. You can also ask on the Stack Exchange Network Engineering site.

Unit Tests

Travis CI project tests shconfparser on Python versions 2.7 through 3.7.

Click the image below for details; the current build status is:
< build: passing image >

License and Copyright

shconfparser is licensed MIT; 2016-2018

Author and Thanks

shconfparser was developed by Kiran Kumar Kotari


