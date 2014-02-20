#!/usr/bin/python

import argparse
import json
import os

config_file_name = ".deploy_conf"
batch_file_name  = ".deploy_batch"
ignore_file_name = ".deploy_ignore"
m_description    = "Easily deploy to a remote webserver over ftp"
m_epilog         = "Config file: " + config_file_name + "     Ignore File: " + ignore_file_name

def initArgparse():
	"""Initializes the argparse module

	Sets up the argparse module that is used to parse command line arguments.  The two arguments
	that are initialezed are: type, a positional argument which is the name of the configuration
	to run; and --init, an optional argument that signals the program to initialize the config
	and ignore files.
	"""
	parser = argparse.ArgumentParser(epilog=m_epilog,description=m_description)
	parser.add_argument('type', nargs='?',help="which deployment", type=str)
	parser.add_argument('--init', 
		help="Initialize deploy in the current working directory", action='store_true')
	return parser

def init(cli_args):
	"""Checks if the --init argument was passed in the commandline

	Uses the args paramater to check if the --init argument was passed into the command line and if
	it is valid.  The --init argument is valid iff the ignore and config file do not exist.  If at
	least one of the files do not exist, the user will be prompted if they want to overwrite the 
	existing files.  If the user chooses to not overwrite the files, the program will exit, else it
	will return true.

	Args:
		cli_args: Namespace object returned from ArgumentParser.parse_args()

	Returns:
		A Boolean object that is true iff the --init argument was supplied by the user and it is
		valid.
	"""
	# check if user specified init argument
	if not cli_args.init:	
		return False			# init argument was not specified

	# User specified the init argument, check if it is valid

	if ignoreFileExists() or configFileExists():
		res = raw_input("Deploy files already exists. Overwrite?(y/n):_\b")
		if 'n' in res:
			exit()				# user chose to not overwrite the existing files
		elif 'y' in res:
			return True			# user chose to overwrite existing files
		else:
			return None			# user did not make a valid choice
	else:
		return True				# niether the ignore file or the config file exist


def initFiles():
	""" Initializes the deployIgnore and deployConfig files
	"""
	makeIgnoreFile()
	makeConfigFile()
	print "deploy has been initialized, please edit the config file."

def makeConfigFile():
	# TODO(Tyler): Docstring
	f = open(config_file_name,'w')
	f.write("{\n\t\"host\": \"host_address\",\n");
	f.write("\t\"username\": \"username\",\n");
	f.write("\t\"port\": \"port (optional)\",\n");
	f.write("\t\"development\": {\n");
	f.write("\t\t\"root_path\": \"path/to/development_root\"\n");
	f.write("\t}\n");
	f.write("}");
	f.close()

def makeIgnoreFile():
	# TODO(Tyler): Docstring
	f = open(ignore_file_name,'w')
	f.write("# deploy files\n")
	f.write(ignore_file_name + "\n")
	f.write(config_file_name + "\n")
	f.write(batch_file_name + "\n")
	f.close()

def ignoreFileExists():
	# TODO(Tyler): Docstring
	return os.path.isfile(ignore_file_name)

def configFileExists():
	# TODO(Tyler): Docstring
	return os.path.isfile(config_file_name)

def parse_config():
	config_file = open(config_file_name, "r")
	config_json = json.load(config_file)
	lines = list()
	for key in config_json:
		print config_json[key], type(config_json[key])
	



def main():
	parser = initArgparse()
	args =parser.parse_args()

	# if the init argument is specified and valid, create the init files and exit

	if init(args):
		makeConfigFile()
		makeIgnoreFile()
		exit()


	# if init is not specified, then the type argument is required.
	# We check if the argument was passed, if it was not, we show the user the help document and exit
	
	if args.type is None:						
		parser.print_help()
		exit()

	parse_config()



if __name__ == '__main__':
	main()