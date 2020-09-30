#James Elliott
#8.14.2020
#All pdf functions for AutoCount go here

import pandas as pd
import csv
import codecs
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os
import time
import ast

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

################################################################
##############IMPORTANT WORD LISTS##############################

division_keywords = ["SECTION 00","SECTION 26","SECTION 27","SECTION 28"]
search_length = 20 #used to control how far into each page the filter searches


def important_page_filter(pdfFile,output_folder=r'.\\'):
	"""
	takes a .pdf file and returns number of pages and saves pages
	in a given directory location
	"""
	#############################################
	#CHECK OUTPUT_FOLDER# --- DEBUG PURPOSE

	#print("output folder:\n",output_folder)

	#############################################
	#access and collect meta data of a pdf#
	with open(pdfFile, 'rb') as f:
		pdf = PdfFileReader(f)
		information = pdf.getDocumentInfo()
		number_of_pages = pdf.getNumPages()

	txt = f"""
	Information about {pdfFile}: 

	Author: {information.author}
	Creator: {information.creator}
	Producer: {information.producer}
	Subject: {information.subject}
	Title: {information.title}
	Number of pages: {number_of_pages}
	"""
	print(txt)

	#################################################
	#SPLITTING EACH PDF TO A SEPERATE INSTANCE#######
	page_title = "pdfPage_"
	pdf = PdfFileReader(pdfFile)
	final_page_list = [] #list used to append pdf's together at end after filtering through pages.
	final_section_list = {} #disctionary of section numbers that are important to us
	for page in range(number_of_pages):


		#if (page % 100) == 0:
		print("On Page:",page)


		pdf_writer = PdfFileWriter()
		pdf_writer.addPage(pdf.getPage(page))

		current_page = page_title + str(page+1)
		full_path = output_folder + r"\\" + current_page + ".pdf"

		with open(full_path,"wb") as output_pdf:
			pdf_writer.write(output_pdf)
########START OF TEXT EXTRACTION &&& Important Page Finder#########################	
		word_data = convert_pdf_to_txt(full_path)
		word_list = word_data.splitlines()
			#print("word list equals the following:\n",word_list)
		#List of strings collected, below uses search algorithm to decide if a page is worth keeping or not#
		header = header_search(division_keywords, word_list)
		if header != None:
			#list of page numbers with headers/End of Sections
			final_section_list[header] = "" #///////////////////////////////////////////////////////////////////BROKEN////////////////////////////////#

		include_section = section_search(final_section_list, word_list)
		if include_section == True:
			final_page_list.append(page+1)

		try:
			os.remove(full_path)
		except:
			print("Could not delete file")
		finally:
			pass
	print("FINAL PAGE LIST:", final_page_list)
	print("FINAL SECTION LIST\n",final_section_list)
	###################################################################
	########MERGE IMPORTANT PAGES######################################
	final_pdf = PdfFileWriter()
	final_path = r".\important_divisions.pdf"
	for page in final_page_list:
		try:
			final_pdf.addPage(pdf.getPage(page-1))
		except:
			print("page:",page,"was not added to final_pdf")
	with open(final_path,"wb") as output_pdf:
			final_pdf.write(output_pdf)


	return final_page_list

def header_search(keyword_list, page_list):
	"""
	Searches and Returns Section Header
	"""
	header_search_range = {"space":8,"no_space":6}
	offset = 8 #number of offset letters to get to the spec number starting position
	keyword_found = False
	header = ""

	try:
		for phrase in keyword_list:
			for pdf_line in range(search_length):
				line = page_list[pdf_line]
				start_letter = line.find(phrase)
				if start_letter != -1: #keyword implies SECTION 26,27,28, etc
					keyword_found = True
					start = start_letter+offset #start of numbers
					space_checker = line[start + 2]

					try:
						if space_checker.isspace() == True:
							print("is_space")
							header_length = header_search_range.get("space")
						else:
							print("no_space")
							header_length = header_search_range.get("no_space")
					except:
						print("error with space_checker --- line 125 of specsheetcontrols")
						print("space checker = ",space_checker)
						print("start of numbers = ",start)
					finally:
						pass


					for letter in range(start,start + header_length): #plus one needed because starts at 0
						try:
							header = header + line[letter]
						except:
							print("header index out of range\nSaving header as one letter")
							print(page_list)
						finally:
							pass
						return header
	except:
		print("error with header_search")
	finally:
		pass

def section_search(section_list,page_list):
	"""
	searches for section number in a list of strings
	"""
	keyword_found = False
	sections = list(dict.fromkeys(section_list))
	for phrase in sections:
		for pdf_line in range(search_length):
			line = page_list[pdf_line]
			is_found = line.find(phrase)
			if is_found != -1:
				keyword_found = True
				return keyword_found
	return keyword_found


def convert_pdf_to_txt(path, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(path, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


##########################################################
##########################################################
##########################################################
def empty_line_remover(txtFile):
	"""
	removes lines with only spaces from a .txt file
	INPUT: txtFile
	"""
	tmp = open(txtFile,"r",encoding="utf-8")
	searchable_string = tmp.readlines()
	loop_str = searchable_string
	#print(len(searchable_string))

	final_instances = []
	for line in range(len(loop_str)):
		if loop_str[line] == '\n' or loop_str[line] == ' \n' or loop_str[line][0] == r"\\":
			searchable_string[line] = "we FAILED"

	final_instances = list(dict.fromkeys(searchable_string))

	#print(final_instances)
	for line in final_instances:
		if line == "we FAILED":
			final_instances.remove(line)
	return final_instances	



##########################################
###########start of script################

if __name__ == '__main__':

	#pdf = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\PDFtest\Div. 27&28 Specs_Volume1.pdf"
	pdf = r"S:\Shared Folders\Steven\Quotes\6000\6072 Sac Court House\02_Project Manual\SPC-VOL 03_V1.pdf"
	output_folder = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\PDFtest\split"

	important_page_filter(pdf,output_folder)
########################################################
#TO DO LIST --> HAVE IT JUST LOOP THROUGH BEGINNING OF PAGE FOR FIRST LOOP
#LOOP THROUGH END OF PAGE FOR LAST LOOP
#should make the time much,much LESS for ripping out important pages.
#And than do tedious searches within those pages for more detailed findings