# fastfield main python script.

## change enviroment variable
## activate 'walker'

import json
import pickle as pck
import os
import shutil

class event_handler():
	def __init__ (self,events = []):
		self.events = list(events)
	
	def update_handler(self, new_event):
		"""takes in event name and adds it to events log if it doesn't exist"""
		if new_event in self.events:
			return None
		self.events.append(new_event)
	def pickle_save(self,pickle_path,file_name="event_list.pkl"):
		complete_path = os.path.join(pickle_path,file_name)
		save_file = open(complete_path,"wb")
		pck.dump(self.events,save_file)
		save_file.close()
def open_event_handler(event_pkl_path):
	"""
	Helper Function to Open an Already existing event handler and return instant of event_handler
	"""
	loaded_list = pck.load(event_pkl_path)
	handler = event_handler(events=loaded_list)
	return handler

class open_JSON():
	def __init__(self,json_file):
		self.json_file_location = json_file
		self.json_info = self.open_json(json_file)
		self.job_num = self.get_field("JI_job_number")
		self.daily_date = self.get_field("JI_dailyDate")
		self.job_name = self.get_field("JI_project_name")

	@staticmethod
	def open_json(file_path):
		"""opens .json file"""
		with open(file_path,encoding="utf-8") as f:
			info = json.load(f)
		return info

	def get_field(self,job_field):
		return self.json_info[job_field]

#use after database analysis
class move_JSON(open_JSON):
	def __init__(self,open_JSON,job_dir):
		# open_JSON class instantiation
		self.JSON = open_JSON

		# sub-dir extraction
		self.dir = job_dir
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
		new_file = "".join([self.JSON.job_name,"_",str(self.JSON.job_num),"_" ,str(self.JSON.daily_date[0:9]),"_Construction_Daily.json"])
		new_file = self.__remove_special_characters(new_file) #remove illegal characters

		job_folder_path = os.path.join(self.dir,str(self.JSON.job_num))
		complete_save_path = os.path.join(job_folder_path,new_file)

		if str(self.JSON.job_num) not in self.existing_jobs:
			os.mkdir(job_folder_path)
		os.replace(self.JSON.json_file_location,complete_save_path)

def organize_json_dir(json_dir,job_dir):
	"""uses open_JSON & move_FILE classes over a directory to organize all files into given job folder"""
	json_files = [f for f in os.listdir(json_dir) if f.endswith(".json")]
	for f in json_files:
		json_loaded = open_JSON(os.path.join(json_dir,f))
		move_class = move_JSON(json_loaded,job_dir)
		move_class.move_file()
	print("All Files Moved")

def main():
	# input_dir = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\FastField_Management\JSON_Files_WalkerOriginalForm\Active Construction Daily"
	# job_directory = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\FastField_Management\JSON_Files_WalkerOriginalForm\Job_Directory"
	# organize_json_dir(input_dir,job_directory)

if __name__ == '__main__':
	main()