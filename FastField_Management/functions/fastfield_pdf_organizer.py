# fastfield main python script.

## change enviroment variable
## activate 'walker'

import json
import pickle as pck
import os
import shutil

#use after database analysis
class move_FILE():
	def __init__(self,input_dir,output_file_name,output_dir):
		# open_JSON class instantiation
		self.output_file_name = output_file_name
		self.input_path = os.path.join(input_dir,output_file_name)

		self.job_num = output_file_name[0:output_file_name.find("_")]

		# sub-dir extraction
		self.dir = output_dir
		self.existing_jobs = self.get_job_nums(self.dir)

	@staticmethod
	def get_job_nums(job_dir):
		job_nums = [f for f in os.listdir(job_dir) if not os.path.isfile(os.path.join(job_dir,f))]
		return job_nums
	@staticmethod
	def __create_folder(self,folder_name):
		os.mkdir(os.path.join(self.dir,folder_name))
	@staticmethod
	def __remove_special_characters(file_name,special_char=":][}{/\)(",new_char="_"):
		"""takes input string, and replaces all special_char with new_char"""
		for char in special_char:
			file_name = file_name.replace(char,new_char)
		return file_name
	
	def move_file(self):
		new_file = self.__remove_special_characters(self.output_file_name) #remove illegal characters

		job_folder_path = os.path.join(self.dir,str(self.job_num))
		complete_save_path = os.path.join(job_folder_path,new_file)

		if str(self.job_num) not in self.existing_jobs:
			os.mkdir(job_folder_path)
		os.replace(self.input_path,complete_save_path)

def organize_files(input_dir,job_dir,file_ext=".pdf"):
	"""uses open_JSON & move_FILE classes over a directory to organize all files into given job folder"""
	input_files = [f for f in os.listdir(input_dir) if f.endswith(file_ext)]
	if input_files == []:
		print("No New Files Found")
		return None

	for f in input_files:
		move_class = move_FILE(input_dir,f,job_dir)
		move_class.move_file()
	return True

def main(input_dir = r"S:\Personal Folders\FTP\Dailys",
		daily_pdfs_dir = r"S:\Personal Folders\Job Dailys"):
	NEW_FILE_FLAG = organize_files(input_dir,daily_pdfs_dir)
	return NEW_FILE_FLAG #used with high level main

if __name__ == '__main__':
	main()