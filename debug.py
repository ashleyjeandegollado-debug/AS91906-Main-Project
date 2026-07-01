"""QUICK DEBUG MODULE

	This module provides some quick functions for debug output
	both to the screen and/or to a log file.
	
	Devlin Sakey - 2026
"""
from datetime import datetime   #Datetime Handling
import time
import os

# This is the cumulative debug "level" where all lower levels will apply.
DEBUG_LEVEL=0
# Similar to debug level, but applies to the delay functions, when it's useful to have the program slow down.
# set separately, as  the debug "level of detail" and slowdowns for diagnostic purposes might have different circumstances.
DELAY_LEVEL=0
# This is the filename for the error logging functions
ERROR_LOG=None

def set_debug_level(debug_level):
	"""Set the debug level. This will set the debug level - primarily intended for when
	not using the dot notation"""
	global DEBUG_LEVEL
	try:
		if debug_level > 0:
			DEBUG_LEVEL = int(debug_level)
	except:
		dprint( 0, "set_debug_level - This function expects an integer >= 0" )

def set_delay_level(delay_level):
	"""Set the delay level. This will set the delay level - primarily intended for when
	not using the dot notation"""
	global DELAY_LEVEL
	try:
		if delay_level > 0:
			DELAY_LEVEL = int(delay_level)
	except:
		dprint( 0, "set_delay_level - This function expects an integer >= 0" )

def set_error_log(file_name):
	if len(file_name)>0:
		ERROR_LOG = file_name
	else:
		ERROR_LOG = None

def _logtime():
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _filename_logtime():
	return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def _build_path(path):
# will recursively construct a directory tree
# expects \\ on the end of the path if the last item is a directory.
	dprint(5,"build path:", path)
	directory=os.path.dirname(path)
	dprint(5,"directory:", os.path.splitdrive(directory)[1])
	if len(os.path.splitdrive(directory)[1])>1:
		_build_path(directory)
		if not os.path.exists(directory):
			dprint(4, "creating directory:", directory)
			os.makedirs(directory) # I haven't made any attempt to trap this... The program SHOULD die if this can't happen.

def dsleep(level,sleeptime):
	"""Debug Sleep
	- dsleep(<debug level>, <sleep time>)
	- Specified in seconds. For inserting delays into the program at a specified debug level."""
	if level<=DELAY_LEVEL:
		time.sleep(sleeptime)
	
def dprint(level,*arg):
	"""Debug Print
	- dprint(<debug level>, <items to print. Similar to "print")
	- Outputs items to screen at specified debug level."""
	if level<=DEBUG_LEVEL:
		if level>0:
			print("  " * level, *arg)
		else:
			print( *arg )

def fprint(level, log_path, *arg ):
	"""Debug File Print
	- fprint(<debug level>, <file path>, <items to print. Similar to "print")
	- Outputs items to a file at specified debug level."""
	if level<=DEBUG_LEVEL:
		_build_path(log_path)
		with open(log_path, 'a', encoding="utf-8") as f:
			print(*arg, file=f)

def lprint(level, log_path, *arg ):
	"""Debug LOG File Print
	- fprint(<debug level>, <file path>, <items to print. Similar to "print")
	- Outputs items to a file with a timestamp at specified debug level."""
	if level<=DEBUG_LEVEL:
		_build_path(log_path)
		fprint(level, log_path, _logtime() + " -" * level, *arg)			

def eprint(level, *arg):
	"""Debug Log File Print
	- eprint(<debug level>, <file path>, <items to print. Similar to "print")
	- Outputs items to the error log with a timestamp at specified DEBUG_LEVEL level."""
	if level<=DEBUG_LEVEL and not ERROR_LOG is None:
		print(" *" * level, *arg)
		lprint(level, ERROR_LOG, *arg)
	else:
		print("--- Fatal Error --- \nERROR_LOG has not been set.")
		exit(0)

def bprint(screen_level, file_level, file_name, *arg):
	"""Debug Screen and Log File Print
	- fprint(<debug level>, <file path>, <items to print. Similar to "print")
	- Passing no items to print to this will print a line without a date to the log
	- Pass a null string ("") to print just a date."""
	if not (type(screen_level) == int and type(file_level) == int):
		print(" --- FATAL ---\n'bprint' function expects TWO debug levels.. one for the screen, one for the file")
		exit(0)
	dprint(screen_level, *arg)
	if len(arg)==0:
		fprint(file_level, file_name, *arg)
	else:
		lprint(file_level, file_name, *arg)

