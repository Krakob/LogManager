################################
## Spiral Knights guild log manager
## A collection of tools used to preform various
## tasks on Spiral Knights guild log exports.
## 
## Can also be used as a Python module by simply
## importing this Python file into another script.
##
## Spiral Knights forums thread: 
## GitHub repository: https://github.com/jakobs98/LogManager
################################


################################
## Imports
################################
import os
import sys
import csv


################################
## Variables
################################
header = ['Timestamp', 'Category', 'Name', 'Message']


################################
## Functions
################################
def read_log(filename): #Returns filename as a list of dicts.
    with open(filename) as f:
        return list(csv.DictReader(f))
        #TODO: deal with messages of the day which break the CSV,
        #i.e. contain the sequence of characters ' "," ' or similar.

def format_excel(log_data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, header, delimiter='\t')
        writer.writeheader()
        writer.writerows(log_data)


################################
## Main code
################################
if __name__ == '__main__':
    format_excel(read_log('testlog.csv'), 'excelformat.csv')