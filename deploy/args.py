import sys

class CommandParser(object):

	def __init__(self, name, help_callback=None, help_string=None):
		self.commands = list()
		self.name = name
		self.help_callback = help_callback
		self.help_string = help_string

	def add_command(self, command, cmd_help, callback, args=None):
		self.commands.append({command:callback, 
			'args': args,
			'help':cmd_help, 
			"cmd":command})

	def parse_args(self):
		if len(sys.argv) > 1:
			if sys.argv[1] == 'help' or sys.argv[1] == '-h' :
				self.show_help()
			else:
				for cmd in self.commands:
					if sys.argv[1] in cmd:
						if len(sys.argv) > 2:
							args = cmd['args']
							if args is None:
								cmd[sys.argv[1]](sys.argv[2:])
							elif type(args) is type(list()):
								cmd[sys.argv[1]](sys.argv[2:], *args)
							elif type(args) is type(dict()):
								cmd[sys.argv[1]](sys.argv[2:], *args)
							else:
								cmd[sys.argv[1]](sys.argv[2:], args)
						else:
							args = cmd['args']
							if args is None:
								cmd[sys.argv[1]](None)
							elif type(args) is type(list()):
								cmd[sys.argv[1]](None, *args)
							elif type(args) is type(dict()):
								cmd[sys.argv[1]](None, *args)
							else:
								cmd[sys.argv[1]](None, args)
						break
		else:
			self.show_help()

	def show_help(self):
		if self.help_callback is not None:
			self.help_callback(self.commands)
		elif self.help_string is not None:
			print self.help_string
		else:
			print "TODO make nice default help"