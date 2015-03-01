'''Spiral Knights guild log manager
A collection of tools used to preform various
tasks on Spiral Knights guild log exports.
 
Designed to be usable as a module.

Developed by Krakob. Additional help from Zeddy.

Spiral Knights forums thread:
	http://forums.spiralknights.com/en/node/108270

GitHub repository:
	https://github.com/jakobs98/LogManager

Variables:
	- HEADER (tuple) - contains the header used in logs.
	- ENTRY_DATETIME_FORMAT (string) - the format of the datetime representation in log entries.
	- LOGNAME_DATETIME_FORMAT (string) - the format of the datetime representation in log filenames.

Classes:
	- LogBase - base class containing methods used by both Guild and Log
	- Guild - a container for logs, to be used for managing and compiling logs
	- Log - a single representation of a log file
	- Entry - an entry in a log
	- Timeframe - a period of time

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
import re
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

	def get_dictlist(self):
		'''Gets a list of dicts of the entries in the object.
		'''

		return [entry.get_dict() for entry in self.entries]

	def dump_excel(self, filename):
		'''Dumps Excel appropriate data in filename.
		'''

		with open(filename, 'w', newline='') as f:
			writer = csv.DictWriter(f, HEADER, delimiter='\t', doublequote=False, escapechar='')
			writer.writeheader()
			writer.writerows(self.get_list())


class Guild(LogBase):
	'''A class intended to carry the data from one or more logs for a single guild.
	'''
	
	def __init__(self, logs):
		'''Constructor. Takes a list of Log objects.
		'''

		self.logs = logs

	@classmethod
	def from_files(cls, files):
		'''Alternative constructor. Takes a list of files
		and puts them in the regular constuctor.
		'''

		logs = [Log.from_file(filename) for filename in files]

	@classmethod
	def from_dir(cls, directory, pattern):
		'''Alternative constructor. Takes a directory
		and puts the files in it which match the pattern
		in the from_files constructor.
		'''

		files = []
		for filename in os.listdir('./%s' % directory):
			pass
			# TODO: implement checking for pattern matches
			#		throw list in from_files consturctor


class Log(LogBase):
	'''A single log file, to be contained in a Guild object.
	'''
	
	def __init__(self, entries):
		'''Constructor. Takes a list of Entry objects.
		'''

		self.entries = entries
		self.source = None

	@classmethod
	def from_dictlist(cls, dictlist):
		'''Alternative constructor. Converts a list of dicts to Entry objects
		and puts them in the regular constructor.
		'''

		return cls([Entry.from_dict(entry) for entry in dictlist])

	@classmethod
	def from_file(cls, filename):
		'''Alternative constructor. Derives a list of dicts from a file
		and puts them in the from_dictlist constructor.
		'''

		with open(filename) as f:
			log = cls.from_dictlist(list(csv.DictReader(f)))
			log.source = filename
			log.derive_timeframe()
			return log

	def derive_timeframe(self):
		try:
			print("Trying to derive start and end time based on the filename, %s" % self.source)
			t = datetime.datetime.strptime(' '.join(self.source.split('_')[-2:]) + settings['input_timezone'], LOGNAME_DATETIME_FORMAT)
							# Derive timestamp from filename
			self.timeframe = Timeframe.from_delta(t, datetime.timedelta(days=-10))
			print("Success!")
		except:
			print("Fail! The filename might not be correct (only filenames formatted like the files originally exported from SK work)")
			print("The first and last dates found in the file will be used instead.")
			self.timeframe = Timeframe(self.entries[-1].time, self.entries[0].time)


class Entry:
	'''An entry (line) in a log, to be contained in a Log object.
	'''
	
	def __init__(self, timestamp, category, name, message):
		self.timestamp = timestamp
		self.category = category
		self.name = name
		self.message = message

		self.time = datetime.datetime.strptime(timestamp + settings['input_timezone'], ENTRY_DATETIME_FORMAT + '%z')
						# Create a timezone aware datetime object
						# to represent the time properly.

	@classmethod
	def from_dict(cls, entry_dict):
		return cls(entry_dict['Timestamp'], entry_dict['Category'], entry_dict['Name'], entry_dict['Message'])

	def get_dict(self):
		'''Returns a dictionary containing the information the entry was originally given.
		'''
		
		return {
			'Timestamp': self.timestamp,
			'Category': self.category,
			'Name': self.name,
			'Message': self.message
		}


class Timeframe:
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

	def __str__(self):
		return str(self.start) + " to " + str(self.end)

	def __contains__(self, time):
		'''Checks whether time is within the period of time of the object.
		Usage: if datetime_obj in timeframe
		'''
		
		return self.start <= time <= self.end

	@classmethod
	def from_delta(cls, start, enddelta):
		return cls(start, start+enddelta)



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

	l = Log.from_file('testlog.csv')
	print(l.get_list())