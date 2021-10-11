# JSON reader & Panda Creator + Updater
import json
import pandas as pd
import os
from typing import List
from new_daily_handler import event_main

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
	def __init__(self,json_file_dir,event_handler_files:List = None):
		"""takes in a list of json file names, and their directory, and returns a list of open jsons in a list"""
		self.dir = json_file_dir
		if event_handler_files == None:
			self.files = self.grab_files(self.dir,file_ext=".json")
		else:
			#code for event_handler updating instead of combining all files
			self.files = event_handler_files
		# combine list of .jsons into a singular list of jsons
		self.complete_paths = [os.path.join(self.dir,f) for f in self.files] #hard path joiner
		self.json_records = [single_json.json_info for single_json in [open_JSON(json_obj) for json_obj in self.complete_paths]]
	def to_existing_dataframe(self,existing_csv_path):
		"""append new json's to an existing dataframe()"""
		dataset = pd.read_csv(existing_csv_path)
		new_data = self.to_dataframe()
		final_dataset = dataset.append(new_data)
		# print(f"existing data shape:{dataset.shape}")
		# print(f"new data shape: {new_data.shape}")
		# print(f"Updated Dataset Shape: {final.shape}")
		return final_dataset
	def to_dataframe(self):
		"""returns pandas dataframe and saves it file inside dir"""
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
def raw_json_event_only_combiner(json_dir_path = r"S:\Personal Folders\FTP\Dailys",
	database_dir = r"S:\Personal Folders\Databases"):
	"""Appends .json files to existing dataset only if they haven't been added before.
	new_daily_handler.py holds all information regarding the event_handler used"""
	handler_files = event_main() #grabs files that are not in dataset
	print(f"New Files:\n{handler_files}")

	json_list = json_combiner(json_dir_path,event_handler_files=handler_files)	
	updated_dataset = json_list.to_existing_dataframe(os.path.join(database_dir,"Raw_Dataset.csv"))

	updated_dataset.to_csv(os.path.join(database_dir,"Raw_Dataset.csv"))
	updated_dataset.to_excel(os.path.join(database_dir,"Raw_Dataset.xlsx"))
	print("Raw Dataset Updated")

def raw_json_combiner_main(json_dir_path = r"S:\Personal Folders\FTP\Dailys",
	database_dir = r"S:\Personal Folders\Databases"):
	"""Main Function for combining json's inside the same folder"""
	json_list = json_combiner(json_dir_path)
	
	data_joined = json_list.to_dataframe()
	data_joined.to_csv(os.path.join(database_dir,"Raw_Dataset.csv"))
	data_joined.to_excel(os.path.join(database_dir,"Raw_Dataset.xlsx"))
	print("Raw Dataset Updated")

if __name__ == '__main__':
	# event_main()
	# single_json()
	raw_json_combiner_main()