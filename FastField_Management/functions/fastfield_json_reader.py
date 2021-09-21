# JSON reader & Panda Creator + Updater

import json
import pandas as pd
import pickle as pck
import os
import shutil
from typing import List

class event_handler:
	def __init__ (self,events = []):
		self.events = list(events)
	
	def update_handler(self, new_event):
		"""takes in event name and adds it to events log if it doesn't exist"""
		if new_event in self.events:
			return None
		self.events.append(new_event)
		return True
	def pickle_save(self,pickle_path,file_name="event_list.pkl"):
		if not pickle_path.endswith(".pkl"):
			complete_path = os.path.join(pickle_path,file_name)
		else:
			complete_path = pickle_path
		save_file = open(complete_path,"wb")
		pck.dump(self.events,save_file)
		save_file.close()

class events_loader(event_handler):
	def __init__(self,input_dir,pickle_complete_file):
		self.input_dir = input_dir
		self.pickle_complete_file = pickle_complete_file

		initial_events = self.grab_files(input_dir,file_type=".json")
		super().__init__(self.open_event_handler(pickle_complete_file))

		self.new_files = [f for f in initial_events if f not in self.events] #grab files not in events
		print(f"New files: {self.new_files}")
		self.pickle_save(pickle_complete_file)
		#FIX ERROR WHERE NOT SAVING/NOT OPENING THE SAVED EVENTS?

	@staticmethod
	def open_event_handler(event_pkl_path):
		"""
		Helper Function to Open an Already existing event handler and return instant of event_handler
		"""
		try:
			loaded_list = pck.load(event_pkl_path)
			handler = event_handler(events=loaded_list)
			return handler
		except:
			print("Event Handler Does Not Exist. Please make sure your event_pkl_path is correct.\
				If this is your first run of the event_handler, please run 'initialize_handler'.")
			print("returning empty event_handler")
			return []
	@staticmethod
	def grab_files(input_dir,file_type=".json"):
		"""Grab all files of a specified type"""
		json_files = [f for f in os.listdir(input_dir) if f.endswith(file_type)]
		return json_files
	
def hard_reset():
	"""saves an empty pickle [], so you can rerun on all .JSONs"""
	instance = event_handler()
	instance.pickle_save(database_dir,file_name="daily_list.pkl")

def initialize_handler():
	"""Run event handler to recreate an entire Dataset"""
	hard_reset()
##############################END OF EVENT HANDLER#####################################
class open_JSON():
	def __init__(self,json_file):
		self.json_file_location = json_file
		self.json_info = self.open_json(json_file)
		# self.job_num = self.get_field("JI_job_number")
		# self.daily_date = self.get_field("JI_dailyDate")
		# self.job_name = self.get_field("JI_project_name")

	@staticmethod
	def open_json(file_path):
		"""opens .json file"""
		with open(file_path,encoding="utf-8") as f:
			info = json.load(f)
		return info

	def get_field(self,job_field):
		return self.json_info[job_field]
	def print_all_fields(self):
		for idx, field in enumerate(self.json_info):
			print(f"field {idx}: {field}")

class json_combiner(open_JSON):
	def __init__(self,json_file_dir):
		"""takes in a list of json file names, and their directory, and returns a list of open jsons in a list"""
		self.dir = json_file_dir
		self.files = self.grab_files(self.dir,file_ext=".json")
		self.complete_paths = [os.path.join(self.dir,f) for f in self.files] #hard path joiner
		#create list of information from json files in the complete_paths list
		self.json_records = [single_json.json_info for single_json in [open_JSON(json_obj) for json_obj in self.complete_paths]]
	
	def to_dataframe(self,filename="json_data.pkl"):
		"""returns pandas dataframe and saves it file inside dir"""
		save_path = os.path.join(self.dir,filename)
		self.dataframe = pd.DataFrame.from_records(self.json_records)
		return self.dataframe
	@staticmethod
	def grab_files(input_dir,file_ext=".json"):
		"""grabs all files of a specified type from a directory"""
		input_files = [f for f in os.listdir(input_dir) if f.endswith(file_ext)]
		return input_files
	def __print__(self,var_title,variable_name):
		print(f"Variable Tital {var_title}\n:{variable_name}")


def event_main():
	input_dir = r"S:\Personal Folders\FTP\Dailys"
	database_dir = r"S:\Personal Folders\Databases"
	daily_events_file = r"daily_list.pkl"
	events_loader(input_dir,os.path.join(database_dir,daily_events_file))

def single_json():
	input_json_path = r"S:\Personal Folders\FTP\Dailys\6087_Amazon warehouse stockton_Daily_09_07_2021.json"
	json_cls = open_JSON(input_json_path)
	print(json_cls.json_info)

def raw_json_combiner_main():
	"""Main Function for combining json's inside the same folder"""
	json_dir_path = r"S:\Personal Folders\FTP\Dailys"
	database_dir = r"S:\Personal Folders\Databases"
	json_list = json_combiner(json_dir_path)
	
	data_joined = json_list.to_dataframe()
	data_joined.to_csv(os.path.join(database_dir,"Raw_Dataset.csv"))
	data_joined.to_excel(os.path.join(database_dir,"Raw_Dataset.xlsx"))
	print("Raw Dataset Updated")

if __name__ == '__main__':
	# event_main()
	# single_json()
	raw_json_combiner_main()