import argparse

m_description = "Easily deploy to a remote webserver over ftp"
parser = argparse.ArgumentParser(description=m_description)
parser.add_argument('destination', metavar="destination_name",nargs='?',help="which deployment", type=str)
parser.add_argument('--init', 
	help="Initialize deploy in the current working directory", action='store_true')

def get_destination():
	args = parser.parse_args()
	return args.destination

def get_init():
	args = parser.parse_args()
	return args.init

def show_help():
	parser.print_help()
