from args import CommandParser
from config import Config
from config import ConfigError
import os
from sftp import Sftp

def get_files(config, directory='.'):
	file_dict = dict()
	file_list = list()
	for f in os.listdir(directory):
		if config.ignore(f):
			continue
		if os.path.isfile(directory + "/" + f):
			file_list.append(f)
		elif os.path.isdir(directory + "/" + f):
			retrurned_files = get_files(config, directory=directory + "/" + f)
			file_list.append(retrurned_files)
	file_dict[directory] = file_list
	return file_dict

def handle_config_error(e):
	if e.cause is ConfigError.INVALID_NAME_ERROR:
		print "the supplied name is not valid."
	elif e.cause is ConfigError.NO_NAME_ERROR:
		print "A destination name is required."
	elif e.cause is ConfigError.JSON_ERROR:
		print "Config file is not properly formatted."
	exit()


def init(options, config):
	if config.config_file_exists():		#check if the stuff already exists and handle the stuff
		print "config file already exists"
		return
	else:
		config.create_config_template()
		print "Config file created"
		return

def push(options, config):
	def help():
		print "push all tracked files to the remote"
		print "usage: deploy push [<remote] [<options>]\n"
		print "\t-r\t\tremove all files that are not locally tracked NOT FUNCTIONAL"

	if options is None or len(options) == 1:
		if options is not None and options[0] == 'help':
			help()
			return
		else:
			if config.config_file_exists():		# if it does try to use it, show help if
				try:
					if options is None:
						config.load_config(options)
					else:
						config.load_config(options[0])	# error occurs
				except ConfigError, e:
					handle_config_error(e)
				
			else:
				print "No Config file found, use 'deploy init' to create a sample config file."
				return
	file_dict = get_files(config)
	sftp = Sftp(config.get_destination_root(), file_dict)
	sftp.send_files(config.get_user(), config.get_host())

def main(name="deploy"):
	#dest = args.get_destination()
	#init = args.get_init()
	config = Config()
	cParser = CommandParser(name)
	cParser.add_command('init', 'init help', init, config)
	cParser.add_command('push', 'push help', push, config)
	cParser.parse_args()

	
	"""
	if init:
		if config.config_file_exists():		#check if the stuff already exists and handle the stuff
			print "config file already exists"
			exit()
		else:
			config.create_config_template()
			print "Config file created"
			exit()
	else:
											# go to config and check if file exists, 
		if config.config_file_exists():		# if it does try to use it, show help if
			try:
				config.load_config(dest)	# error occurs
			except ConfigError, e:
				handle_config_error(e)
				
		else:
			print "No Config file found, use 'deploy --init' to create a sample config file."
			exit()
	# everthing is set up i think,
	# implement sftp here
	
	sftp = Sftp(config.get_destination_root(), file_dict)
	sftp.send_files(config.get_user(), config.get_host())
	"""





