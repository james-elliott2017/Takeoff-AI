# Project Management Tools Main
# James Elliott

# from highlight_extractor.highlight_main import highlight_parser
# from drawings_img_add.watermark_main import watermark
# worklog converter import needs to happen; but class structure needs to be created first


#Backend Functions
from highlight_extractor.highlight_main import highlight_parser
from drawings_img_add.watermark_main import watermark

#GUI controls
import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font as tkFont
from tkinter import Y
from PIL import ImageTk, Image

#OS controls
import sys
import os

default_input_pdf = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\ProjectManagementTools\drawings_img_add\example_files\test_page.pdf"
default_output_pdf = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\ProjectManagementTools\drawings_img_add\output_folder\output_pdf.pdf"

class input_header(tk.Frame):
	def __init__(self, master=None):
	    super().__init__(master)
	    self.master = master
	    self.pack()
	    self.create_widgets()

	def create_widgets(self):
		###################### WATERMARK ALL PAGES #####################################
		self.waterMarkALL = tk.Button(self,text="RUN\n(All Pages)",fg="green")
		self.waterMarkALL["command"] = lambda: self.run_AllPages_WaterMark_Includer()
		self.waterMarkALL.grid(row = 0,column = 0,pady=20,ipady=5,ipadx=10)

		######################   EXIT BUTTON   ###########################################
		self.quit = tk.Button(self, text="QUIT", fg="red",
			command=self.master.destroy).grid(row = 0,column = 1,
				ipady=10,ipadx=20,sticky="W")
		#################	INPUT PDF LOCATION  #######################
		self.input_pdf_label = tk.Label(self)
		self.input_pdf_label["text"] = "Input PDF Location"
		self.input_pdf_label.grid(row = 1,column = 0)

		self.input_pdf_entry = tk.Entry(self)
		self.input_pdf_entry['width'] = len(default_input_pdf)
		self.input_pdf_entry.insert(-1,default_input_pdf)
		self.input_pdf_entry.grid(row = 1,column = 1,sticky="W")

		self.change_pdf = tk.Button(self)
		self.change_pdf["text"] = "Select Folder"
		self.change_pdf["command"] = lambda: self.Entry_new_file_location(self.input_pdf_entry)
		self.change_pdf.grid(row = 2,column = 0)

		###################OUTPUT EXCEL LOCATION#########################################
		self.output_excel_label = tk.Label(self)
		self.output_excel_label["text"] = "Output PDF Location"
		self.output_excel_label.grid(row = 3,column = 0)

		self.output_excel_entry = tk.Entry(self)
		self.output_excel_entry['width'] = len(default_input_pdf)
		self.output_excel_entry.insert(-1,default_output_pdf)
		self.output_excel_entry.grid(row = 3,column = 1,sticky="W")

		self.change_excel = tk.Button(self)
		self.change_excel["text"] = "Select Folder"
		self.change_excel["command"] = lambda: self.Entry_new_file_location(self.output_excel_entry)
		self.change_excel.grid(row = 4,column = 0)

	def Entry_new_file_location(self,internal_widget):
		"""updates text of specific widget"""
		internal_widget.delete(0,last=len(internal_widget.get()))
		new_file = tk.filedialog.askopenfilename()
		internal_widget.insert(-1,new_file)

	def run_AllPages_WaterMark_Includer(self):
		"""Runs watermark_class on all pages"""
		pass

class coord_section(tk.Frame):
	def __init__(self, master=None,coord_section_title="Title"):
	    super().__init__(master)
	    self.master = master
	    self.pack()
	    self.title = coord_section_title
	    self.create_widgets()

	def create_widgets(self):
		self.title = tk.Label(self,text=self.title,
			font=tkFont(size=14)).grid(row=0,column=0,columnspan=4,sticky="nsew")

		self.logo_index = tk.Label(self,text="top,left corner").grid(row=1,column=0,columnspan=2)
		self.logo_size = tk.Label(self,text="size").grid(row=1,column=2,columnspan=2)

		self.logo_x = tk.Label(self,text="X: ").grid(row=2,column=0) #C0
		self.logo_y = tk.Label(self,text="Y: ").grid(row=3,column=0) #C0
		
		self.logo_x_input = tk.Entry(self)
		self.logo_x_input.grid(row=2,column=1) #C1
		self.logo_y_input = tk.Entry(self)
		self.logo_y_input.grid(row=3,column=1) #C1


		self.logo_w = tk.Label(self,text="W: ").grid(row=2,column=2) #C2
		self.logo_y = tk.Label(self,text="H: ").grid(row=3,column=2) #C2
		
		self.logo_w_input = tk.Entry(self)
		self.logo_w_input.grid(row=2,column=3) #C3
		self.logo_h_input = tk.Entry(self)
		self.logo_h_input.grid(row=3,column=3) #C3

class update_button(tk.Frame):
	def __init__(self, master=None):
	    super().__init__(master)
	    self.master = master
	    self.pack()
	    self.create_widgets()

	def create_widgets(self):
		self.update_button = tk.Button(self,text="Update\nPreview")
		self.update_button.grid(row=0,column=0,ipady=10,ipadx=10)

class ScrollableImage(tk.Frame):
	def __init__(self, master=None,**kw):
		watermark_class = watermark()
		root_dir = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\ProjectManagementTools\drawings_img_add"
		watermark_class.update_dir(new_working_dir=root_dir)

		img_loc = watermark_class.pixmap_preview()
		self.image = ImageTk.PhotoImage(Image.open(img_loc))


		sw = kw.pop('scrollbarwidth', 10)
		super(ScrollableImage, self).__init__(master=master, **kw)
		self.cnvs = tk.Canvas(self, highlightthickness=0, **kw)
		self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
		# Vertical and Horizontal scrollbars
		self.v_scroll = tk.Scrollbar(self, orient='vertical', width=sw)
		self.h_scroll = tk.Scrollbar(self, orient='horizontal', width=sw)
		# Grid and configure weight.
		self.cnvs.grid(row=0, column=0,  sticky='nsew')
		self.h_scroll.grid(row=1, column=0, sticky='ew')
		self.v_scroll.grid(row=0, column=1, sticky='ns')
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		# Set the scrollbars to the canvas
		self.cnvs.config(xscrollcommand=self.h_scroll.set, 
		                   yscrollcommand=self.v_scroll.set)
		# Set canvas view to the scrollbars
		self.v_scroll.config(command=self.cnvs.yview)
		self.h_scroll.config(command=self.cnvs.xview)
		# Assign the region to be scrolled 
		self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
		self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)

	def mouse_scroll(self, evt):
	    if evt.state == 0 :
	        self.cnvs.yview_scroll(-1*(evt.delta), 'units') # For MacOS
	        self.cnvs.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
	    if evt.state == 1:
	        self.cnvs.xview_scroll(-1*(evt.delta), 'units') # For MacOS
	        self.cnvs.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows

class coord_combined(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		logo_coordinates = coord_section(master=window,coord_section_title="Logo Coordinates")
		logo_coordinates.pack(side='left',anchor="nw")

		white_box_coordinates = coord_section(master=window,coord_section_title="White Box Coordinates")
		white_box_coordinates.pack(side='left',anchor="nw")
		self.pack()

def __scrollbar_add(window):
	scrollbar = tk.Scrollbar(window)
	scrollbar.pack( side = 'right', fill=Y ) 
	 
	mylist = tk.Listbox(window, yscrollcommand = scrollbar.set ) 
	for line in range(100): 
	   mylist.insert('end', str(line))
	 
	mylist.pack( side = 'left', fill = 'both' ) 
	scrollbar.config(command = mylist.yview)


if __name__ == "__main__":
	window = tk.Tk()
	window.title("Add Logo Interface")
	screen_width = window.winfo_screenwidth()
	screen_height = window.winfo_screenheight()
	window.geometry(f"{int(screen_width*.75)}x{int(screen_height/2)}")

	__scrollbar_add(window)

#############PACKING SEPERATE FRAMES TOGETHER###########################
	header = input_header(master=window)
	header.pack(side='top',anchor="nw")

	coords = coord_combined(master=window)
	coords.pack(side='left',anchor="nw")	

	updateButton = update_button(master=window)
	updateButton.pack(side='top',anchor="nw")
	
	images = ScrollableImage(master=window)
	images.pack(side='top',anchor="nw")

	window.mainloop()

	#TO DO LIST
	# 1) Connect Coordinates and Input location to a run command for appending
	# 2) Give option to open file when finished
	# 3) Progress Bar
	# 4) Implent image box method