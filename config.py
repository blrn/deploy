import json
import os
import re

class ConfigError(Exception):
	JSON_ERROR = "JSON"
	NO_NAME_ERROR = "NO_NAME"
	INVALID_NAME_ERROR = "INVALID_NAME"
	def __init__(self, msg, cause):
		self.msg = msg
		self.cause = cause

class Config(object):
#TODO: docs!
	def __init__(self, config_file_name=".deploy_conf"):
		self.config_file_name = config_file_name

	def config_file_exists(self):
		return os.path.isfile(self.config_file_name)

	def load_config(self, name=None):
		#raises ConfigError: json
		#raises IOError
		config_file = open(self.config_file_name)
		try:
			config_dict = json.load(config_file)
			config_file.close()
			self.parse(config_dict, name)
		except ValueError, e:
			raise ConfigError("json error", ConfigError.JSON_ERROR)
		

	def create_config_template(self):
		template = os.path.dirname(os.path.realpath(__file__)) + "/template/conf_template.json"
		dest = os.getcwd() + "/" + self.config_file_name
		self.__copy_file(template,dest)


	def __copy_file(self,source_path, dest_path):
		#raises IOError
		source = open(source_path,'r')
		dest = open(dest_path,'w')
		for line in source:
			dest.write(line)
		source.close()
		dest.close()

	def ignore(self, filename):
		# returns true if it matches any of the ignores
		if self.ignore_files is not None:
			if filename in self.ignore_files:
				return True
		if self.ignore_ext is not None:
			file_list = filename.split('.')
			if file_list[len(file_list) - 1] in self.ignore_ext:
				return True
		if self.ignore_group is not None:
			for pat in self.ignore_group:
				result = re.search(pat,filename)
				if result is not None:
					return True
		return False

	def parse(self, config_dict, name=None):
		#raises KeyError
		#raises ConfigError
		if name is None and len(config_dict['targets']) != 1:
			raise ConfigError("name must be specified with more than one configuration", ConfigError.NO_NAME_ERROR)
		self.host = config_dict['host']
		self.user = config_dict['username']
		if 'port' in config_dict:
			self.port = config_dict['port']

		target = None
		if name is None:
			target = config_dict['targets'][0]
		else:
			for t in config_dict['targets']:
				if t['name'] == name:
					target = t
					break
		if target is None and name is None:		# might be unreachable
			raise ConfigError("No valid configuration found.", ConfigError.JSON_ERROR)
		elif target is None:
			raise ConfigError("No configuration was found with the given name", ConfigError.INVALID_NAME_ERROR)

		self.root_path = target['root_path']
		if "ignore" in target:
			#TODO: DOCS!
			ignore = target['ignore']
			if 'file' in ignore:
				self.ignore_files = ignore['file']
			if 'group' in ignore:
				self.ignore_group = ignore['group']
			if 'extension' in ignore:
				self.ignore_ext = ignore['extension']