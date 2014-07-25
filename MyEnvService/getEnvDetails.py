#!/usr/bin/python
import sys

# =======================================================================================
# Script to provide wrapper to currentENV.py
# This will loop through all parameters from currentENV.py for readability
# Created     :         getkub@github 
program =    sys.argv[0]
version =    "1"
verdate =    "2014-02-22T13:02:00Z"
#      Version    Date      Comment
#       1       2014-03-04 Initial Version
# =======================================================================================
module_path              =    os.path.dirname(os.path.dirname(os.path.dirname(program)))

# This will ensure relevant path is appended to current path
sys.path.append(module_path)

from module_path import currentENV.py

hostparams=env_ThisHost()

sorted = hostparams.items()
sorted.sort()
for k,v in sorted:
    print k + '=' + v
