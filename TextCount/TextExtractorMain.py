#TestExtractorMain.py
#pdf_extractor

import os
import shutil
import pandas as pd
import json
from typing import List

class JSON_EditError(Exception):
	def __init__(self,json_path: str):
		super().__init__(f"Json file either has empty division, does not exists, or is corrupted. Please update JSON file:\n{json_path}")

class create_default_json:
	def __init__(self):
		"""default json for projects, used to create json file for  new projects"""
		self.json_dict = {
			"default":["search_1","search_2"]
		}
	def __create_json(self,save_dir,name="Constants.json"):
		complete_path = os.path.join(save_dir,name)
		with open(complete_path,'w') as f:
			json.dump(self.json_dict,f)

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
			with open(self.json_path,'w') as f:
				json.dump({},f)
			constants = {}
		return constants

	def add_division(self,division: str, search_list: List = []):
		"""add new division including constants if appicable"""
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
	
	def __isDivision(self,division: str):
		"""returns True if division exists"""
		if division in self.constants.keys():
			return True
		return False

	def load_division_words(self,division: str) -> List:
		"""returns specific constants for TextCount from loaded JSON"""
		division_words = self.constants[division]
		return division_words

	def save_json(self):
		"""Resave the opened JSON"""
		with open(self.json_path,'w') as f:
			json.dump(self.constants,f)

	def print_json(self,add_message: str=""):
		"""Debug Helper: Prints the Classes JSON File"""
		print(f"{add_message}Dictionary:\n{self.constants}")
	def grab_all_divisions(self):
		"""return list of all divisions found inside .json in"""
		divisions = [div for div in self.constants.keys()]
		print(f"Found Divisions: {divisions}")
		return divisions

	def count_main(self,division: str):
		if (self.__isDivision(division) == True) and (self.load_division_words(division) != []):
			return self.load_division_words(division)
		else:
			self.save_json()
			raise JSON_EditError(self.json_path)

class text_counter():
	def __init__(self,
	takeoff_AI_root_dir = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI"
	):
		self.takeoffAI_root_dir = takeoff_AI_root_dir
		#^ROOT PROJECT DIRECTORY---CHANGE THIS!!!^#

		###LOCAL HARD PATHS###
		self.project_dir = os.path.join(self.takeoffAI_root_dir,"Walker Projects")
		self.MainExtractionFolder = r"TextExtractor_files"
		self.text_folder_local = r"text_folder"
		self.csv_folder = r"csv_folder"
		#Subfolders per Division
		self.sub_folders = ["text_folder","csv_folder"]

		#.CSV Save Information
		self.csv_default = "Total_Counts.csv"
		self.header_default = "Total Counts"
	def __repr__(self):
		self.name = "text_counter()"
		return "{} class instance".format(self.name)

	def __csv_write(self,my_dict,header,project_folder,csv_fileName = "project_counts.csv"):
		if project_folder:
			if csv_fileName == "project_counts.csv":
				save_location = os.path.join(project_folder,"project_counts.csv")
				(pd.DataFrame.from_dict(data=my_dict, orient='index')
				   .to_csv(save_location, header=header))
			else:
				tmp = csv_fileName.replace(".txt", ".csv")
				save_location = os.path.join(project_folder,tmp)
				(pd.DataFrame.from_dict(data=my_dict, orient='index')
				   .to_csv(save_location, header=header))
		elif csv_fileName != "project_counts.csv":
			pass
		else:
			(pd.DataFrame.from_dict(data=my_dict, orient='index')
			   .to_csv(header=header))

	def __dictionaryMerger(self,list_of_dictionaries):
		"""
		ONLY WORKS IF DATA IS NUMBERS
		Function takes in list of dictionaries and than merges the two by adding together the combination of same key names
		"""
		final_dictionary = {}
		for page in list_of_dictionaries:
			#print(page)
			for key in page:
				if key in final_dictionary:
					final_dictionary[key] = final_dictionary[key] + page[key]
				else:
					final_dictionary[key] = page[key]

			#if final_dictionary[page]
		return final_dictionary

	def __pdfExtractor(self,file: str):
		"""
		Exports data as list and uppercase
		"""
		a_file = open(file, "r")#,encoding="utf-8")
		list_of_lists = []
		for line in a_file:
			try:
				line = str.upper(line)
				stripped_line = line.strip()
				line_list = stripped_line.split()
				list_of_lists.append(line_list)
			except:
				print(f"the following line failed to be cleaned:\n{line}")

		a_file.close()

		return list_of_lists

	def __ratioManipulator(self,single_dictionary,ratio):
		for term in single_dictionary:
			tmp_num = single_dictionary.get(term)
			single_dictionary[term] = single_dictionary[term] * ratio
		return single_dictionary

	def __wordFinder(self,key_word,ratioManipulator_Output):
		"""
		print every time a specific word is found in a list of list.
		key_word: word to search
		ratioManipulator_Output: designed to work with self.__ratioManipulator Function
			If you don't use the function --> this input must be a "list of lists"
		"""
		str1 = key_word
		for phrase in ratioManipulator_Output:
			for word in phrase:
				if word.find(str1) == 0:
						print(word)

	def MainTextExtractor(self,csv_save_folder: str,searchable_list: List[str],ratio: bool = False):
		"""
		main function to extract counts based on words searched for

		csv_save_folder: folder to save .csv files in
		searchable_list: key words to search for in the text file
		ratio: False implies no scaling (INPUT MUST BE DICTIONARY W/FILE LABELS --- I.E. text_file_T1.1.1_"mark_A1".txt)
			Example: ratio = {'A1':15,'A2':2,'A3':3,'B1':6,'B2':2,'B3':8,'C1':1}
			"mark" is the marking, can not be changed
			"add term for each different 'key' to seperate multiple pages"
		"""
		files_list = os.listdir(self.text_folder_global)

		total_counts = []
		for file in files_list:
			total_addy = self.text_folder_global + r"\\" + file
			#print(total_addy)

			#print(files_list)
			j = self.__pdfExtractor(total_addy)
			#print(j)
			
			d = {}
			#print("LIST:\n", searchable_list)
			for item in searchable_list:
				count = 0
				for phrase in j:
					for word in phrase:
						if item == word:
							count = count + 1
				d[item] = count
			
			##########################
			#######RATIO CODE############RATIO FUNCTION TO HANDLE ROOM SCALING
			if ratio != False:
				##############################FIX LATER --- NEEDS TO TAKE RATIO, MULITPLY, RETURN, AND THAN BE NEW SAVED
				
				####INPUT EXAMPLE ONLY#############################
				#ratio = {'A1':15,'A2':2,'A3':3,'B1':6,'B2':2,'B3':8,'C1':1}
					#print("FILE:",file)
				for key in ratio:
					if file.find(key) != -1:
						#print(n)
						#print(ratio[key])
						d = self.__ratioManipulator(d, ratio[key])
				##################################################

			#print(d)
			total_counts.append(d)
			self.__csv_write(d, "NA", csv_save_folder,csv_fileName=file)
		###Make sure to give correct files to change with given ratio


		#filter for all pages to combine counts
		complete_counts = self.__dictionaryMerger(total_counts)
		#print(complete_counts)
		filtered_counts = {}
		for item in complete_counts:
			if complete_counts.get(item) != 0:
				filtered_counts[item] = complete_counts[item]

		#print("COMPLETE\n",complete_counts)
		print("FILTERED\n",filtered_counts)
		#print(len(filtered_counts))
		self.__csv_write(filtered_counts, self.header_default, csv_save_folder,csv_fileName=self.csv_default)
		print("Counts Complete")

	def divisionCreator(self,working_dir: str,division: str):
		"""
		Creates sub-division for text extraction (I.E. - AV,Low Voltage, Fire, Security, etc.)

		working_dir: location to save .txt & save .csv files too (inside "TextExtractor_files")
		division: sub_folder name
		"""
		path = os.path.join(working_dir,division)
		os.mkdir(path)
		for folder in self.sub_folders:
			complete_path = os.path.join(path,folder)
			os.mkdir(complete_path)

	def textExtracMain(self,Project: str,division: str):
		"""
		Main program to run for text_extraction. Take the given project (must already be created via AutoCount)
			and than creates division or visits that division and runs counts based on inputed text_files
		"""
		print("DISCLAIMER: TextExtractorMain will be phased out in new version. Please use textExtracMain_V2_JSON() for newer code")
		#WORKING Directory for textExtraction files
		self.txtMainDir = os.path.join(self.project_dir, Project ,self.MainExtractionFolder)
		try:
			import sys
			sys.path.append(self.txtMainDir)
			import Constants
			print(Constants)
			print("Constants Load Successful")
		except:
			print("text_constants do NOT exist for",Project)
			print("creating text_constants file, please add constants to file")
			constant_copy_path = os.path.join(self.txtMainDir,"Constants.py")

			self.constants_template = r"text_constants.py"
			self.templateDir = os.path.join(self.takeoffAI_root_dir,r"TextCount")
			completeConstantPath = os.path.join(self.templateDir,self.constants_template)
			print(f"test: {completeConstantPath}")
			shutil.copyfile(completeConstantPath, constant_copy_path)
			#time.sleep(1)
			import sys
			sys.path.append(self.txtMainDir)
			import Constants
			print(Constants.words)



		#.txt files location
		self.text_folder_global = os.path.join(self.txtMainDir,division,self.text_folder_local)
		 #.csv files location
		self.csv_save_folder = os.path.join(self.txtMainDir,division,self.csv_folder)
		try:
			#edit if using different names in class:words
			#############################################
			#Low Voltage
			#print(Constants.words.LowVoltage)
			keyWords = Constants.words.AV_Ceiling # Change this to loading a .json
				#load json, 'constants':[key_words]
	################################################################################################################
			self.MainTextExtractor(self.csv_save_folder,keyWords)
		except:
			print("FOLDER DOES NOT EXIST, creating new one")
			
			self.divisionCreator(self.txtMainDir, division)
			#FINAL VERSION --- put self.divisionCreator() in same .py as project creator for organization
			print("path created\nPlease Rerun Script")

	def textExtracMain_V2_JSON(self,Project: str,division: str) -> None:
		"""Same as textExtracMain but uses JSON's to save and load constants data"""
		#WORKING Directory for textExtraction files
		self.txtMainDir = os.path.join(self.project_dir, Project ,self.MainExtractionFolder)
		#Check if Project Folder Exists
		try:
			self.divisionCreator(self.txtMainDir, division)
			print("Division Folder DOES NOT EXIST, created new one. Rerun")
		except:
			pass
		
		# walker job folder setup .txt files location
		self.text_folder_global = os.path.join(self.txtMainDir,division,self.text_folder_local)
		x = os.path.join(self.txtMainDir,division)
		# walker job folder .csv save location
		self.csv_save_folder = os.path.join(self.txtMainDir,division,self.csv_folder)

		#Load Text_Search_List from JSON
		json_path = os.path.join(self.txtMainDir,"Constants.json")
		text_class = text_variables(json_path) #json_class initialization
		keyWords = text_class.count_main(division)

		#run text counter
		self.MainTextExtractor(self.csv_save_folder,keyWords)
	def main_V2_allDivisions(self,Project):
		"""same as textExtractMain_V2_JSON, but loops through all divisions"""
		#WORKING Directory for textExtraction files
		self.txtMainDir = os.path.join(self.project_dir, Project ,self.MainExtractionFolder)

		# Load JSON class
		json_path = os.path.join(self.txtMainDir,"Constants.json")
		text_class = text_variables(json_path) #json_class initialization
		# grab all divisions
		all_divisions = text_class.grab_all_divisions()
		#loop through textExtracMain_V2_JSON
		div_class = text_counter()
		for div in all_divisions:
			print(f"Division Start: {div}")
			div_class.textExtracMain_V2_JSON(Project,div)

def main_V2(project):
	"""Loops through all divisions inside the .JSON for the given project"""
	

	main_class = text_counter()
	# Run through all divisions inside a .json
	main_class.main_V2_allDivisions(project)

def main_V1():
	project = r"6082 Sunnyville Civic Center"
	division = r"LowVoltage"

	main_class = text_counter()
	main_class.textExtracMain(project, division)

def main_V2_w_PDFtoTxt(project:str,rectangle,save_dir,input_pdf,output_txt = r"output.txt"):
	pass

if __name__ == "__main__":
	project = r"6082 Sunnyville Civic Center"
	main_V2(project)