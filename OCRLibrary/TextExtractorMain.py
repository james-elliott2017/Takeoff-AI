#TestExtractorMain.py
#pdf_extractor

import os
import shutil
import time
import numpy as np
import pandas as pd
import re

class text_counter():
	def __init__(self):
		self.takeoffAI_root_dir = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI"
		#^ROOT PROJECT DIRECTORY---CHANGE THIS!!!^#

		###LOCAL HARD PATHS###
		self.project_dir = os.path.join(self.takeoffAI_root_dir,"Walker Projects")
		self.MainExtractionFolder = r"TextExtractor_files"
		self.text_folder = r"text_folder"
		self.csv_folder = r"csv_folder"
		#Subfolders per Division
		self.sub_folders = ["self.text_folder","self.csv_folder"]

		#.CSV Save Information
		self.csv_default = "Total_Counts.csv"
		self.header_default = "Total Counts"

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

	def __pdfExtractor(self,file):
		"""
		Exports data as list and uppercase
		"""
		a_file = open(file, "r",encoding="utf-8")

		list_of_lists = []
		for line in a_file:
			line = str.upper(line)
			stripped_line = line.strip()
			line_list = stripped_line.split()
			list_of_lists.append(line_list)

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

	def MainTextExtractor(self,csv_save_folder,searchable_list,ratio = False):
		"""
		main function to extract counts based on words searched for

		csv_save_folder: folder to save .csv files in
		searchable_list: key words to search for in the text file
		ratio: False implies no scaling (INPUT MUST BE DICTIONARY W/FILE LABELS --- I.E. text_file_T1.1.1_"mark_A1".txt)
			Example: ratio = {'A1':15,'A2':2,'A3':3,'B1':6,'B2':2,'B3':8,'C1':1}
			"mark" is the marking, can not be changed
			"add term for each different 'key' to seperate multiple pages"
		"""
		#print("text FOLDER\n",self.text_folder)
		files_list = os.listdir(self.text_folder)
		print("txt Files list:",files_list)

		total_counts = []
		for file in files_list:
			total_addy = self.text_folder + r"\\" + file
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

	def divisionCreator(self,working_dir,division):
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

	def textExtracMain(self,Project,division):
		"""
		Main program to run for text_extraction. Take the given project (must already be created via AutoCount)
			and than creates division or visits that division and runs counts based on inputed text_files
		"""
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
			self.templateDir = os.path.join(self.takeoffAI_root_dir,r"OCRLibrary")
			completeConstantPath = os.path.join(self.templateDir,self.constants_template)
			shutil.copyfile(completeConstantPath, constant_copy_path)
			#time.sleep(1)
			import sys
			sys.path.append(self.txtMainDir)
			import Constants
			print(Constants.words)



		#.txt files location
		self.text_folder = os.path.join(self.txtMainDir,division,self.text_folder)
		 #.csv files location
		self.csv_save_folder = os.path.join(self.txtMainDir,division,self.csv_folder)
		try:
			#edit if using different names in class:words
			#############################################
			#lowVoltage
			#print(Constants.words.LowVoltage)
			keyWords = Constants.words.data
				#tmp_ratio = {"0_":3,"8_":3,"10_":2,"11_":4}
	################################################################################################################
			self.MainTextExtractor(self.csv_save_folder,keyWords)
		except:
			print("FOLDER DOES NOT EXIST, creating new one")
			
			self.divisionCreator(self.txtMainDir, division)
			#FINAL VERSION --- put self.divisionCreator() in same .py as project creator for organization
			print("path created\nPlease Rerun Script")


if __name__ == "__main__":
	project = r"6082 Sunnyville Civic Center"
	division = r"LowVoltage"

	self.textExtracMain(project, division)