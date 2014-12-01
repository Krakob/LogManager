"""
Spiral Knights guild log manager
A collection of tools used to preform various
tasks on Spiral Knights guild log exports.
 
Designed to be usable as a module.

Developed by Krakob. Additional help from Zeddy.

Spiral Knights forums thread:
	Not yet existent.

GitHub repository:
	https://github.com/jakobs98/LogManager

Variables:
	- header (list)
	- datetime_format (string)

Functions:
	- read_settings(filename)
	- read_log(filename)
	- format_excel(log_data, filename)

TEMP NOTES:
Interesting stuff:
datetime.strptime, datetime.strftime - reading and writing timestamps
datetime.astimezone - conversion to different timezones

datetime.timezone - should be used for target timezone.
"""


################################
## Imports
################################
import os
import sys
import csv
import datetime


################################
## Variables
################################
header = ('Timestamp', 'Category', 'Name', 'Message') #Correctly ordered header for exported logs.
datetime_format = "%m/%d/%y %I:%M:%S %p" #Format of datetime entry. MM/DD/YY HH:MM:SS AM/PM.


################################
## Functions
################################
def input_bool(prompt="Please enter an answer. "):
	'''Asks the user to input yes or no, where they return their respective boolean values.'''
	a = input(prompt+"(y/n)\n")
	while True:
		if a == 'y':
			return True
		elif a == 'n':
			return False
		else:
			print('Error! Input must be "y" (yes) or "n" (no).\n')
			a = input(prompt+"(y/n)\n")

def read_settings(filename):
	"""Returns a dictionary containing data from filename, where the first column contains the key
	and the second second column contains the value.
	The delimiter should be an equals sign (=)"""
	print("Attemtping to read settings from %s." % filename)
	settings = {}
	try:
		with open(filename) as f:
			settings_data = csv.reader(f, delimiter="=")
			for row in settings_data:
				settings[row[0]] = row[1] #Column 0 = key, column 1 = value
			print("The settings were successfully read!")
			return settings
	except FileNotFoundError:
		print("%s could not be found." % filename)

def read_log(filename):
	"""Returns a list of dictionaries containing information from filename, which should be a log exported by Spiral Knights.
	Each dict also gets an additional entry, Timestamp obj, which is a timezone-aware Python datetime object."""
	print("Attempting to read the log %s." % filename)
	try:
		with open(filename) as f:
			log_data = list(csv.DictReader(f))
			for entry in log_data:
				entry['Timestamp obj'] = datetime.datetime.strptime(entry['Timestamp'], datetime_format) #Add a new key to each entry with a timezone-aware datetime object
			print("Success!")
			return log_data
	except FileNotFoundError:
		print("%s could not be found." % filename)

def format_excel(log_data, filename):
	"""Converts log_data to Excel-suitable format (tab separated CSV) and dumps it in filename."""
	excel_data = log_data #Copy log data.
	for entry in excel_data:
		entry['Timestamp'] = entry['Timestamp obj'].strftime(settings['excel_timestamp']) #Overwrite timestamp with excel formatted timestamp.
		del entry['Timestamp obj']
		#print("ENTRY: %s\n" % entry)
	with open(filename, 'w', newline='') as f:
		writer = csv.DictWriter(f, header, delimiter='\t', doublequote=False)
		writer.writeheader()
		writer.writerows(excel_data)


################################
## Main code
################################
if __name__ == '__main__':
	settings = read_settings("settings.csv")
	print(settings)

	log = read_log("testlog.csv")
	format_excel(log, "exceldump.csv")
	