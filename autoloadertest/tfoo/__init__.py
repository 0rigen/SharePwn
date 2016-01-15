# Modified from from http://www.stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python
# The namespaces we want to iterate through recursively must be known in advance
from scanners import *
from aux import *

# Defining what "all" means for "tfoo" allows us to include all sub-modules by importing tfoo
__all__ = ["scanners", "aux"]
