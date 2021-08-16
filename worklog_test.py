#Worklog 2.0 uses box dimensions to grab each item

#IMPORTS#
import os
import numpy as np
import PyPDF2
from PyPDF2 import PdfFileReader
import fitz
import os

import csv

def grab_pdf_files(folder_path, file_type = ".pdf"):
	pdf_files = pdf_list = [f for f in os.listdir(folder_path) if f.find(".pdf") != -1]
	return pdf_files

def __list_to_events(list_of_headers):
	"""converts list of headers to events with header as key, and value as next header"""
	event_dict = {}
	for title_idx in range(len(list_of_headers)-1):
		event_dict[list_of_headers[title_idx]] = list_of_headers[title_idx+1]
	return event_dict


############################################################################################
if __name__ == '__main__':
	#load in .pdf files for pathing
	folder_path = r"C:\Users\james\OneDrive\Documents\Coding Projects\Walker Telecomm Automation\ProjectManagementTools\WorkLog_Converter\pdf_folder"
	pdf_list = grab_pdf_files(folder_path,file_type=".pdf")
	
	pdf_loc = os.path.join(folder_path,pdf_list[0])
	pdf = fitz.open(pdf_loc)
	
	text = pdf.load_page(0)
	text = text.get_text('text')
	print(list(text.split("\n")))

['Project Name','Job Number', 'Report By', 'Date','Weather', 'Notes', 'Current Conditions','Describe Work Accomplished',
'Materials and Equipment On', 'Specification Number', 'Drawing Number', 'Location', 'Description of Exception or', 'Defect', 'Foreman Comments', 'Actual Percentage of Work', 'Completed', 'Projected Completion Date', 'Total Crew Hours Worked', 'List of Employees On Site', 'Andrew', 'Miguel', 'Brian', 'Ryan Linn', 'Additional Comments', 'Sorting the cable is taking a bit longer because of how long and how many other', 'trades moved our bundles around in the room. Should still have them in tomorrow.', 'Date Submitted: 06/15/2021 02:40 PM', 'Submitted By: andrew@walkertelecomm.com', 'Construction Daily', 'Page 1 of 2', '']