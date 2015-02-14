'''Spiral Knights guild log manager
A collection of tools used to preform various
tasks on Spiral Knights guild log exports.
 
Designed to be usable as a module.

Developed by Krakob. Additional help from Zeddy.

Spiral Knights forums thread:
	Not yet existent.

GitHub repository:
	https://github.com/jakobs98/LogManager

Variables:
	- HEADER (tuple) - contains the header used in logs.
	- ENTRY_DATETIME_FORMAT (string) - the format of the datetime representation in log entries.
	- LOGNAME_DATETIME_FORMAT (string) - the format of the datetime representation in log filenames.

Functions:
	- read_settings(filename)
	- read_log(filename)
	- format_excel(log_data, filename)
'''



################################
## Imports
################################
import os
import sys
import csv
import datetime



################################
## Constants (not really :( )
################################
HEADER = ('Timestamp', 'Category', 'Name', 'Message')  # Correctly ordered header for exported logs.

ENTRY_DATETIME_FORMAT = "%m/%d/%y %I:%M:%S %p"  # Format of datetime entry.
												# MM/DD/YY HH:MM:SS AM/PM.

LOGNAME_DATETIME_FORMAT = "%Y-%m-%d %H-%M-%S%z"  # (modified) format of datetime in log filenames. 
												 # YYYY-MM-DD HH-MM-SS+zzzz



################################
## Classes
################################
class LogBase:
	'''Base class containing methods needed by both Guild and Log.
	The class is not meant to be instantiated.
	'''
	
	def format_excel(self, output_filename=None):
		'''Converts all entries to Excel-suitable format (tab separated CSV without quotation marks)
		and dumps it in output_filename if provided. Otherwise just returns a list of dicts of the
		entries in the object.
		'''

		excel_rows = []
		for entry in self.entries:
			excel_rows.append(entry.get_dict())
			# print("ENTRY: %s\n" % entry)
		if output_filename:  # If there is an output filename
			with open(output_filename, 'w', newline='') as f:
				writer = csv.DictWriter(f, HEADER, delimiter='\t', doublequote=False)
				writer.writeheader()
				writer.writerows(excel_rows)
		return excel_rows


class Guild(LogBase):
	'''A class intended to carry the data from one or more logs for a single guild.
	'''
	
	def __init__(self, name):
		self.logs = []
		self.name = name
		# TODO: read all logs in /logs with the guild name provided as the 2nd argument.


class Log(LogBase):
	'''A single log file, to be contained in a Guild object.
	'''
	
	def __init__(self, filename):
		self.entries = []
		self.source = filename

		print("Attempting to read the log %s." % filename)
		try:
			with open(filename) as f:
				log_data = list(csv.DictReader(f))  # Make a list of dicts of all entries in the log.
				for entry in log_data:
					self.entries.append(Entry(entry))  # Make Entry objects for all entries.
				print("Success!")
		except FileNotFoundError:
			print("%s could not be found." % filename)

		try:
			print("Trying to derive start and end time based on the filename, %s" % filename)
			self.end = datetime.datetime.strptime(' '.join(filename.split('_')[-2:]) + settings['input_timezone'], LOGNAME_DATETIME_FORMAT)
			self.start = self.end - datetime.timedelta(weeks=1)
			print("Success!")
		except:
			print("Fail! The filename might not be correct (only filenames formatted like the files originally exported from SK work)")
			print("The first and last dates found in the file will be used instead.")
			self.start = self.entries[-1].time
			self.end = self.entries[0].time


class Entry:
	'''An entry (line) in a log, to be contained in a Log object.
	'''
	
	def __init__(self, entry):
		self.timestamp = entry['Timestamp']
		self.category = entry['Category']
		self.name = entry['Name']
		self.message = entry['Message']

		self.time = datetime.datetime.strptime(entry['Timestamp'] + settings['input_timezone'], ENTRY_DATETIME_FORMAT + '%z')
						# Create a timezone aware datetime object
						# to represent the time properly.
		# This comment is here to retain indentation.

	def get_dict(self):
		'''Returns a dictionary containing the information the entry was originally given.
		'''

		return {
			'Timestamp': self.timestamp,
			'Category': self.category,
			'Name': self.name,
			'Message': self.message
		}


class Timeperiod:
	'''A period of time with a starting and an ending point.
	Provides a method for checking whether a point of time is within it.
	'''

	def __init__(self, start, end):
		if start < end:	 # Make sure that the provided start is before the provided end.
			self.start = start
			self.end = end
		else:
			self.start = end
			self.end = start

	@classmethod
	def from_delta(cls, start, enddelta):
		return cls(start, start+enddelta)

	def contains(self, time):
		'''Checks whether time is within the period of time of the object.
		'''
		return self.start <= time <= self.end



################################
## Functions
################################
def input_bool(prompt="Please enter an answer. "):
	'''Asks the user to input yes or no, where they return their respective boolean values.
	'''
	
	a = input(prompt+"(y/n)\n").lower()
	while True:
		if a == 'y':
			return True
		elif a == 'n':
			return False
		else:
			print("Error! Input must be 'y' (yes) or 'n' (no).\n")
			a = input(prompt+"(y/n)\n").lower()


def read_settings(filename):
	'''Returns a dictionary containing data from filename, where the first column contains the key
	and the second second column contains the value.
	The delimiter should be an equals sign (=)
	'''

	print("Attemtping to read settings from %s." % filename)
	settings = {}
	try:
		with open(filename) as f:
			settings_data = csv.reader(f, delimiter="=")
			for row in settings_data:
				settings[row[0]] = row[1]  # Column 0 = key, column 1 = value
			print("The settings were successfully read!")
			return settings
	except FileNotFoundError:
		print("%s could not be found." % filename)



################################
## Main code
################################
if __name__ == '__main__':
	settings = read_settings("settings.csv")
	print(settings)