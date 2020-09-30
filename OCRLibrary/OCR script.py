#Main Script
#Use this to call all other files

import os
import OCRMain
import cv2
import numpy as np
import pytesseract
from pytesseract import Output

from TextExtractorMain import dictionaryMerger
from TextExtractorMain import csv_write
from text_constants import words


def get_OCR(data,image,searchable_list,highlight_page_number):
	"""
	data: image data for OCR software, needs to be prefiltered with cv2 or equivalent
	image: base image to put highlights on (recommend in color)
	searchable_list: list of terms to search for on pages
	highlight_page_number: counter so that multiple highlights can be saved.
		Give single number if NOT wanting to use
	"""
	wordList = []
	custom_config = r"--psm 6"
	final_list = pytesseract.image_to_data(data,output_type=Output.DICT,config=custom_config)
	#Gives key() parameters if you FORGOT
	#print(final_list.keys())

	n_boxes = len(final_list['text'])
	confirmation_accuracy = 40
	tmp_counts = {}


	for word in range(n_boxes):
			if int(final_list['conf'][word]) > confirmation_accuracy:
				wordList.append(final_list['text'][word])
				#^^^DELETE AFTER EVERYTHING WORKS, ONLY FOR DEBUG PURPOSES^^^#
				###########################################
				########REMOVE IF STATEMENT IF YOU WANT ALL THRESHOLD VISUALY MARKED, IF NOT, ONLY GRAPHS THOSE THAT ARE CORRECT#########
				
					###GRAPHING CODE BELOW###
				if str.upper(final_list['text'][word]) in searchable_list:
					(x, y, w, h) = (final_list['left'][word], final_list['top'][word], final_list['width'][word], final_list['height'][word])
					img = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)
				else:
					(x, y, w, h) = (final_list['left'][word], final_list['top'][word], final_list['width'][word], final_list['height'][word])
					img = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

	#print("PRE:",wordList)
	i = []
	for string in wordList:
		i.append(str.upper(string))
	wordList = i
	
	for part in searchable_list:
		count = 0
		for word in wordList:
			if word == part:
				count = count + 1
		tmp_counts[part] = count
	#print("POST\n",wordList)


	ocr_highlight_folder = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\Walker Projects\6082 Sunnyville Civic Center\Storage\OCR Highlights"
	location = ocr_highlight_folder + "\\" + r"OCRhighlight_"+ str(highlight_page_number) + r".png"
	#print("Save Folder:", location)
	try:
		cv2.imwrite(location, img)
	except:
		print("error writing image, assume no counts found on page")
		#print("tmp_counts:",tmp_counts)
		cv2.imwrite(location,image)
	finally:
		
	################################################
	###DEBUG CODE FOR DICTIONARY LOOP & WORD LIST###
		#print list of words/phrases collected
		#print(wordList)
		#print("KEY:", final_counts.keys())
		#print("count:", final_counts["DMRX"])
		return tmp_counts

def multiplePageOCR(image_folder, part_list,directory_path):
	"""
	image_folder: folder with image files to iterate through
	part_list: List of words you are looking for in the images
	directory_path: directory where images are stored.

	RETURNS: A list of dictionaries. Each dictionary stores counts for each iterated part in "part_list"
	"""


	#use for highlights writing & per page list "TotalCountsList"
	pageNumber = 0
	#used to store counts/page instead of complete total
	TotalCountsList = []

	#########################################################
	############PER IMAGE LOOP FOR ENTIRE FOLDER#############
	for file in image_folder:
		#IMAGE FILTERS, ---selection needs to be creats for args
		completePath = os.path.join(directory_path,file)
		#print(completePath)
		
		image = cv2.imread(completePath)
		gray = OCRMain.get_grayscale(image)
		opening = OCRMain.opening(gray)
		thresh = OCRMain.thresholding(gray)

		final_counts = get_OCR(thresh,image,part_list,pageNumber)

		############################################
		TotalCountsList.append(final_counts)
		print("Page Counts:", TotalCountsList[pageNumber])
		#^^^Must be before pageNumber interation^^^#
		pageNumber = pageNumber + 1
	return TotalCountsList



		

if __name__ == "__main__":
	#MUST USE on windows when using tesseract
	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
	##############################################

#####################################################
#############INPUT LIST & IMAGE FOLDER FOR SEARCHING################
	#searchable_list = ['DMRX', 'MP1', 'LCD', 'CCAM', 'CMIC', 'OFE', 'CPUAWSW16X16', 'VWP', 'TUNER', 'NVR', 'ALS', 'SA',\
	#	 'CTW', 'GMIC', 'CM', 'SBS', 'AVSW', 'VPROJ1', 'LCD80', 'AIR', 'WALL', 'STOWABLE', 'CM', 'DSP', 'SPLIT', 'WMIC', 'PA70', 'CTP', 'PA70-100', 'PA70-200']

	searchable_list = words.key_words
	folder_loc = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\Walker Projects\6081 LAX Transit Building\plans_images"
	directory = os.listdir(folder_loc)
	csv_header = "OCR Counts"
	#print(directory)
#####################################################
#####################################################
	pageCounts = multiplePageOCR(directory, searchable_list,folder_loc)
	print("Final Counts\n",pageCounts)

	totalCounts = dictionaryMerger(pageCounts)
	print("final counts:", totalCounts)
	csv_write(totalCounts, csv_header, r".\\",csv_fileName="OCR_TotalCounts.csv")


###################NEED TO DO###################
#1) Reorganize file management so the folder will create folders for highlights and projects and always work
	#1a Right now the highlights folder and input folder have to be changed manually, makes each job take longer

#REMINDER OF WHERE TO CONTINUE
	#1) SEARCH WORKS and dubug prints are created to make sure list and data are moving correctly
	#2) Need to implement folder loop, but function is already setup
		#MAKE SURE --- to send a counter number into it for highlights not to be overwritten & use for percentage done


	