#WorkLog Converter Main
##Main Python Script to run Walker Telecomm's Worklog Extractor

#James Elliott

#IMPORTS#
import os
import numpy as np
import PyPDF2
from PyPDF2 import PdfFileReader
import csv

def grab_pdf_files(folder_path, file_type = ".pdf"):
	pdf_files = pdf_list = [f for f in os.listdir(folder_path) if f.find(".pdf") != -1]
	return pdf_files

def _section_search(start_stop_sections,complete_txt):
	section_start = complete_txt.find(start_stop_sections[0]) + len(start_stop_sections[0])
	section_end = complete_txt.find(start_stop_sections[1])
	assert section_start != -1, "Section Search Failed to Find: {}".format(start_stop_sections[0])
	assert section_end != -1, "Section Search Failed to Find: {}".format(start_stop_sections[1])

	indexes = [section_start,section_end]
	#print("indexes: ", indexes)

	cleaned = {start_stop_sections[0]: complete_txt[indexes[0]:indexes[1]]}
	return cleaned

def _section_list():
	project_name = ["Project Name","Job Number"]
	job_number = ["Job Number","Report By"]
	person = ["Report By","Date"]
	date = ["Date","Weather"]
	completed_labor = ["Describe Work Accomplished", "Materials and Equipment On"]
	employees_on_site = ["List of Employees On Site","Additional Comments"]
	additional_comments = ["Additional Comments","Date Submitted:"]

	section_search_list = [project_name,job_number,person,date,completed_labor,
							employees_on_site,additional_comments]
	#date = ["Today's Date","rrg"] #NEEDS FIXING
	return section_search_list

def search_text(list_of_startStop,complete_txt):
	#Grab Each Info Section and Organize into Dictionary
	final_dict = {}
	for start_stop in list_of_startStop:
		cleaned = _section_search(start_stop, complete_txt)
		final_dict.update(cleaned)
	return final_dict
def _append_text(PdfReader):
	page_num = PdfReader.numPages
	complete_text = ""
	for i in range(page_num):
		page = PdfReader.getPage(i)
		text = page.extractText()
		complete_text += text
	return complete_text

def single_file_search(pdf_dir,pdf_file_name,
	save_csv = True,csv_file_name = 'worklog.csv'):

	#open .pdf as binary
	complete_path = os.path.join(folder_path,pdf_file_name)
	pdfFileObj = open(complete_path,'rb')
	#open file inside PyPDF2
	PdfReader = PdfFileReader(pdfFileObj)

	if PdfReader.numPages == 1:#print(PdfReader.numPages)
		#extract first page
		page_1 = PdfReader.getPage(0)
		complete_txt = page_1.extractText()
	else:
		complete_txt = _append_text(PdfReader)

	start_stop_sections = _section_list() #load in search variables

	final_dict = search_text(start_stop_sections,complete_txt) #Extract Data in Dictionary Format

	if save_csv == True:
		#save to .csv
		csv_file = open(csv_file_name,"w",newline='')
		writer = csv.writer(csv_file)
		writer.writerow(final_dict.keys())
		writer.writerow(final_dict.values())
		csv_file.close()
		print("File Saved @ ",csv_file_name)

	return final_dict

def multi_file_search(folder_path,pdf_list,csv_file_name = "multi_worklog.csv"):
	#initialize .csv file
	csv_file = open(csv_file_name,"w",newline='')
	writer = csv.writer(csv_file)

	flag = True
	for pdf_file in pdf_list:
		#full_path = os.path.join(folder_path,pdf_file)
		final_dict = single_file_search(folder_path, pdf_file,save_csv=False)

		if flag == True:
			writer.writerow(final_dict.keys())
			writer.writerow(final_dict.values())
			flag = False
		else:
			writer.writerow(final_dict.values())
	csv_file.close()
	print("File Saved @ ",csv_file_name)

# if __name__ == '__main__':
#load in .pdf files for pathing
folder_path = r"C:\Users\james\OneDrive\Documents\Coding Projects\Walker Telecomm Automation\ProjectManagementTools\WorkLog_Converter\pdf_folder"
pdf_list = grab_pdf_files(folder_path,file_type=".pdf")
print("PDF Files Found: ", pdf_list)

final_dict = single_file_search(folder_path, pdf_list[0],
									save_csv=False)
multi_file_search(folder_path, pdf_list)

#print statement
print()
for key in final_dict:
	print("{}: {}".format(key,final_dict[key]))
