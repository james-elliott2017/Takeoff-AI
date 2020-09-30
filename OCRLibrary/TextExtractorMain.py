#TestExtractorMain.py
#pdf_extractor

import os
import shutil
import time
import numpy as np
import pandas as pd
import re

def csv_write(my_dict,header,project_folder,csv_fileName = "project_counts.csv"):
	if project_folder:
		if csv_fileName == "project_counts.csv":
			save_location = project_folder + r"\\" + "project_counts.csv"
			(pd.DataFrame.from_dict(data=my_dict, orient='index')
			   .to_csv(save_location, header=header))
		else:
			tmp = csv_fileName.replace(".txt", ".csv")
			save_location = project_folder + r"\\" + tmp
			#print("save_location:",save_location)
			(pd.DataFrame.from_dict(data=my_dict, orient='index')
			   .to_csv(save_location, header=header))
	elif csv_fileName != "project_counts.csv":
		pass
	else:
		(pd.DataFrame.from_dict(data=my_dict, orient='index')
		   .to_csv(header=header))

def dictionaryMerger(list_of_dictionaries):
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

def pdfExtractor(file):
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

def ratioManipulator(single_dictionary,ratio):
	for term in single_dictionary:
		tmp_num = single_dictionary.get(term)
		single_dictionary[term] = single_dictionary[term] * ratio
	return single_dictionary

def wordFinder(key_word,ratioManipulator_Output):
	"""
	print every time a specific word is found in a list of list.
	key_word: word to search
	ratioManipulator_Output: designed to work with ratioManipulator Function
		If you don't use the function --> this input must be a "list of lists"
	"""
	str1 = key_word
	for phrase in ratioManipulator_Output:
		for word in phrase:
			if word.find(str1) == 0:
					print(word)

def MainTextExtractor(text_folder,csv_save_folder,searchable_list,ratio = False):
	"""
	main function to extract counts based on words searched for

	text_folder: location of text files
	csv_save_folder: folder to save .csv files in
	searchable_list: key words to search for in the text file
	ratio: False implies no scaling (INPUT MUST BE DICTIONARY W/FILE LABELS --- I.E. text_file_T1.1.1_"mark_A1".txt)
		Example: ratio = {'A1':15,'A2':2,'A3':3,'B1':6,'B2':2,'B3':8,'C1':1}
		"mark" is the marking, can not be changed
		"add term for each different 'key' to seperate multiple pages"
	"""
	#print("text FOLDER\n",text_folder)
	files_list = os.listdir(text_folder)
	print("txt Files list:",files_list)

	total_counts = []
	for file in files_list:
		total_addy = text_folder + r"\\" + file
		#print(total_addy)

		#print(files_list)
		j = pdfExtractor(total_addy)
		#print(j)
		
		d = {} #d = dictionary
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
			str1 = ratio
			
			####INPUT EXAMPLE ONLY#############################
			#ratio = {'A1':15,'A2':2,'A3':3,'B1':6,'B2':2,'B3':8,'C1':1}

			tmp_list = []
			if file.find(str1) != -1:
				#print("FILE:",file)
				for key in ratio:
					if file.find(key) != -1:
						#print(n)
						#print(ratio[key])
						d = ratioManipulator(d, ratio[key])
			##################################################

		#print(d)
		total_counts.append(d)
		csv_write(d, "NA", csv_save_folder,csv_fileName=file)
	###Make sure to give correct files to change with given ratio


	#filter for all pages to combine counts
	complete_counts = dictionaryMerger(total_counts)
	#print(complete_counts)
	filtered_counts = {}
	for item in complete_counts:
		if complete_counts.get(item) != 0:
			filtered_counts[item] = complete_counts[item]

	#print("COMPLETE\n",complete_counts)
	print("FILTERED\n",filtered_counts)
	#print(len(filtered_counts))
	csv_write(filtered_counts, "Total Counts", csv_save_folder,csv_fileName="Total_Counts.csv")
	print("Counts Complete")

def divisionCreator(working_dir,division):
	"""
	Creates sub-division for text extraction (I.E. - AV,Low Voltage, Fire, Security, etc.)

	working_dir: location to save .txt & save .csv files too (inside "TextExtractor_files")
	division: sub_folder name
	"""
	sub_folders = ["text_folder","csv_folder"]

	#print(working_dir)
	#print(division)
	path = working_dir + r"\\" + division
	os.mkdir(path)
	for folder in sub_folders:
		complete_path = path + r"\\" + folder
		os.mkdir(complete_path)

def textExtracMain(Project,division):
	"""
	Main program to run for text_extraction. Take the given project (must already be created via AutoCount)
		and than creates division or visits that division and runs counts based on inputed text_files
	"""
	primary_directory = (r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\Walker Projects")
	#^ROOT PROJECT DIRECTORY^#
	###Does not change --- must match divisionCreator() folder names
	slash = r"\\"
	MainExtractionFolder = r"TextExtractor_files"
	text_folder = r"text_folder"
	csv_folder = r"csv_folder"

	#WORKING DIRectory for textExtraction files (DO NOT CHANGE)
	txtMainDir = primary_directory + r"\\" + Project + r"\\" + MainExtractionFolder

	try:
		import sys
		sys.path.append(txtMainDir)
		import Constants
		print(Constants)
		print("Constants Load Successful")
	except:
		print("text_constants do NOT exist for",Project)
		print("creating text_constants file, please add constants to file")
		copy = txtMainDir + "\\" + "Constants.py"


		original = r"text_constants.py"
		originalPath = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\OCRLibrary"
		completeConstantPath = originalPath + r"\\" + original
		shutil.copyfile(completeConstantPath, copy)
		#time.sleep(1)
		import sys
		sys.path.append(txtMainDir)
		import Constants
		print(Constants.words)



	#.txt files location
	text_folder = txtMainDir + r"\\" + division\
	 + r"\\" + text_folder

	 #.csv files location
	csv_save_folder = txtMainDir + r"\\" + division\
	 + r"\\" + csv_folder

	try:
		#edit if using different names in class:words
		#############################################
		#lowVoltage
		#print(Constants.words.LowVoltage)
		keyWords = Constants.words.LowVoltage
################################################################################################################
		MainTextExtractor(text_folder, csv_save_folder,keyWords)
	except:
		print("FOLDER DOES NOT EXIST, creating new one")
		
		divisionCreator(txtMainDir, division)
		#FINAL VERSION --- put divisionCreator() in same .py as project creator for orginization
		print("path created\nPlease Rerun Script")

if __name__ == "__main__":
	project = r"6082 Sunnyville Civic Center"
	division = r"LowVoltage"

	textExtracMain(project, division)