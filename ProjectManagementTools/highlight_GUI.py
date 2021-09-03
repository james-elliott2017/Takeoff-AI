# Project Management Tools Main
# James Elliott

# from highlight_extractor.highlight_main import highlight_parser
# from drawings_img_add.watermark_main import watermark
# worklog converter import needs to happen; but class structure needs to be created first


#Backend Functions
from highlight_extractor.highlight_main import highlight_parser

#GUI controls
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

#OS controls
import sys
import os

default_pdf = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\ProjectManagementTools\highlight_extractor\pdf_input\test_highlight.pdf"
default_excel = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\ProjectManagementTools\highlight_extractor\excel outputs\highlights.xlsx"

class highlight_extractor_frame(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master

		self.create_widgets()
		self.pack()
	    

	def create_widgets(self):
		#################	INPUT PDF LOCATION  #######################
		self.input_pdf_label = ttk.Label(self)
		self.input_pdf_label["text"] = "Input PDF Location"
		self.input_pdf_label.grid(row = 0,column = 0)

		self.input_pdf_entry = ttk.Entry(self)
		self.input_pdf_entry['width'] = len(default_pdf)
		self.input_pdf_entry.insert(-1,default_pdf)
		self.input_pdf_entry.grid(row = 0,column = 2,sticky="W")

		self.change_pdf = ttk.Button(self)
		self.change_pdf["text"] = "Select Folder"
		self.change_pdf["command"] = lambda: self.Entry_new_file_location(self.input_pdf_entry)
		self.change_pdf.grid(row = 1,column = 0)

		###################OUTPUT EXCEL LOCATION#########################################
		self.output_excel_label = ttk.Label(self)
		self.output_excel_label["text"] = "Output Excel Location"
		self.output_excel_label.grid(row = 2,column = 0)

		self.output_excel_entry = ttk.Entry(self)
		self.output_excel_entry['width'] = len(default_pdf)
		self.output_excel_entry.insert(-1,default_excel)
		self.output_excel_entry.grid(row = 2,column = 2,sticky="W")

		self.change_excel = ttk.Button(self)
		self.change_excel["text"] = "Select Folder"
		self.change_excel["command"] = lambda: self.Entry_new_file_location(self.output_excel_entry)
		self.change_excel.grid(row = 3,column = 0)

		###################### RUN HIGHLIGHT TO EXCEL #####################################
		self.highlightExtractor = ttk.Button(self,text="RUN")
		self.highlightExtractor["command"] = lambda: self.run_highlightExtractor()
		self.highlightExtractor.grid(row = 9,column = 0,pady=20,ipady=10,ipadx=20)

		####################### Open Excel after Run #####################################
		self.FLAG_EXCEL_VAR = tk.IntVar()
		self.openExcel_FLAG = ttk.Checkbutton(self,text="Open Excel",variable=self.FLAG_EXCEL_VAR)
		self.openExcel_FLAG.grid(row=9,column=1)

		######################   EXIT BUTTON   ###########################################
		self.quit = ttk.Button(self, text="QUIT",
			command=self.master.destroy).grid(row = 10,column = 0,ipady=10,ipadx=20)

	def Entry_new_file_location(self,internal_widget):
		"""updates text of specific widget"""
		internal_widget.delete(0,last=len(internal_widget.get()))
		new_file = tk.filedialog.askopenfilename()
		internal_widget.insert(-1,new_file)

	def run_highlightExtractor(self):
		###################### RUN COMPLETE/PROGRESS BAR #################################
		self.progressBar = ttk.Label(self,text="Running")
		self.progressBar.grid(row=10,column=2)
		input_pdf = self.input_pdf_entry.get()
		output_excel = self.output_excel_entry.get()
		highlight_class = highlight_parser(input_pdf,output_excel)
		highlight_class.main() #highlights text parser
		self.progressBar.config(text="Complete")

		if self.FLAG_EXCEL_VAR.get() == 1:
			os.startfile(output_excel)

if __name__ == "__main__":
	window = tk.Tk()
	window.title("Highlight Extractor Interface")

	##############beautify code#############
	design_path = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\ProjectManagementTools\sun-valley.tcl"
	window.tk.call("source",design_path)
	window.tk.call("set_theme","dark")
	########################################

	screen_width = window.winfo_screenwidth()
	screen_height = window.winfo_screenheight()
	window.geometry(f"{int(screen_width*.75)}x{int(screen_height/2)}")

	app = highlight_extractor_frame(master=window)
	app.pack()

	window.mainloop()



# TO DO LIST
# 1) Create Super Class to control all functions

