
import os
import shutil
import time
import numpy as np
import pandas as pd
import re
import json
from typing import List

### OUT OF DATE, PLEASE REFER TO TextExtractMain() for up-to-date class version

class text_variables():
	def __init__(self,json_path: str):
		self.json_path = json_path
		# self.constants initialization
		self.constants = self.__initialize_JSON()

	def __initialize_JSON(self):
		"""
		Opens existing JSON, or creates empty dictionary if nothing found.
		Intializes self.constants
		"""
		try:
			with open(self.json_path) as f:
				constants = json.load(f)
			print("JSON Found, loading found JSON")
		except:
			print("JSON Load Failed. Creating Empty JSON & Reloading")
			# with open(self.json_path,'w') as f:
			# 	json.dump({},f)
			constants = {}
		return constants

	def add_division(self,division: str, search_list: List = []):
		"""add new division including constants if applicable"""
		if division in self.constants.keys():
			print(f"Key '{division}' already exists")
		else:
			self.constants[division] = search_list
		
	def update_division(self,division: str,search_list: List = []):
		"""updates already existing division inside JSON"""
		if division in self.constants.keys():
			self.constants[division] = search_list
		else:
			print(f"Division '{division}' does NOT exist")

	def load_division_constants(self,division):
		"""returns specific constants for TextCount from loaded JSON"""
		division_constants = self.constants[division]
		return division_constants

	def save_json(self):
		"""Resave the opened JSON"""
		with open(self.json_path,'w') as f:
			json.dump(self.constants,f)

	def print_json(self,add_message: str=""):
		"""Debug Helper: Prints the Classes JSON File"""
		print(f"{add_message}Dictionary:\n{self.constants}")

def test_main():
	work_dir = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\Walker Projects\6081 LAX Transit Building\TextExtractor_files"
	json_file = r"6081_Constants.json"
	file_path = os.path.join(work_dir,json_file)

	PA = ["S1","S2","S3","S4","M1"]
	Security = ["CAT6A","TRAVELING","PTZ","180","FIXED","COMPOSITE","22-4"]
	PA_diagram = ["RM-MP12A","EOL","CROWN","2903315","RD-ADA4D","RD-ADA8D","BLU-326","ANS501","FRA2C1M1","RM-MP12A"]

	constants = text_variables(file_path)
	constants.print_json()

	constants.add_division("PA",PA)
	constants.add_division("Security",Security)
	constants.print_json(add_message="Post Add Test\n")
	constants.save_json()
	constants = text_variables(file_path)
	constants.print_json(add_message="Reload Test, Changes should be same as above\n")

	constants.update_division("doesn't exist")

	extracted = constants.load_division_constants("PA")
	print(f"Load Constants Output of 'PA': {extracted}")

	constants.save_json()

if __name__ == '__main__':
	test_main()