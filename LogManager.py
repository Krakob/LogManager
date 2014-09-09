################################
## Spiral Knights guild log manager
## A collection of tools used to preform various
## tasks on Spiral Knights guild log exports.
## 
## Can also be used as a Python module by simply
## importing this Python file into another script.
##
## Spiral Knights forums thread: 
## GitHub repository: 
################################


################################
## Imports
################################
import os
import sys
import csv


################################
## Functions
################################
def read_log(filename): #Returns filename as a list of dicts.
    with open(filename) as f:
        return list(csv.DictReader(f))
		

################################
## Main code
################################
if __name__ == "__main__":
    print(read_log("testlog.csv"))