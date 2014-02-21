import copy
import os

class Sftp(object):

	def __init__(self, destination_path, file_dict):
		self.destination = destination_path
		self.file_dict = file_dict

	def send_files(self, user, host):
		self.user = user
		self.host = host
		print self.user
		print self.host
		batch_file = open(".deploy_batch", 'w')
		batch_file.write("cd " + str(self.destination) + "\n")
		self.__make_batch_file(batch_file)
		batch_file.write("bye")
		batch_file.close()
		batch_file = open(".deploy_batch", "r")
		print "batch_file:"
		for line in batch_file:
			print line.rstrip()
		batch_file.close()
		cmd = "sftp -b " + ".deploy_batch" + " " + user + "@" + host
		print cmd
		os.system(cmd)
		os.remove(".deploy_batch")


	def __prepare_remote_deploy(self):
		batch_file.write("cd " + str(self.destination) + "\n")


	def __make_batch_file(self, batch_file, directory='.', file_dict=None):
		if file_dict is None:
			file_dict = self.file_dict
		if(directory is not '.'): # TODO: fix this, wont work if destination ends in /
			batch_file.write("! ssh " + self.user + "@" + self.host + " \"mkdir -p " + self.destination + "/" + directory +"\""+"\n" )
			batch_file.write("cd " + directory[directory.rfind('/')+1:len(directory)] +"\n")
			batch_file.write("lcd " + directory[directory.rfind('/')+1:len(directory)] +"\n")
		#print "directory:", directory
		#print "file_dict: ", file_dict
		for f in file_dict[directory]:
			if isinstance(f,dict):
				#print "f:", f
				dir_path = copy.deepcopy(f).popitem()[0]
				self.__make_batch_file(batch_file, dir_path, file_dict=f)
			else:
				batch_file.write("put " + f + "\n")
		batch_file.write("cd ..\n")
		batch_file.write("lcd ..\n")

		"""
		batch_file = open(".deploy_batch")
		batch_file.write("cd " + self.destination_path + "\n")
		for directory in self.file_dict:
			batch_file.write("cd " + directory + "\n")
			batch_file.write("")
			for f in file_dict['directory']:
				batch_file.write("put " + f + )
		"""