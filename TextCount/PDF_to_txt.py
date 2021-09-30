import os
import fitz

class pdf_to_txt():
	def __init__(self,save_directory: str,pdf_location: str,bounding_box = None):
		self.dir = save_directory
		self.pdf_location = pdf_location
		self.pdf_obj = self.__open_pdf()

		self.text_rect = bounding_box #if None searches whole page
	def update_text_rect(self,new_rect: tuple):
		"""x0,y0,x1,y1 should be integers"""
		x0,y0,x1,y1 = new_rect
		self.text_rect = fitz.Rect(x0,y0,x1,y1)

	def __open_pdf(self):
		"""given pdf_location, open a fitz pdf object"""
		pdf_obj = fitz.open(self.pdf_location)
		return pdf_obj

	def __grab_text(self,fitz_page):
		page_text = fitz_page.get_text("text",clip=self.text_rect,flags=0)
		return page_text
	def save_pixmap(self,page_num=0):
		pixmap = self.pdf_obj[page_num]
		pixmap = pixmap.getPixmap()
		pixmap.writeImage(os.path.join(self.dir,"output.png"))
	def view_pixmap(self,windows_pc = True):
		"""opens pixmap output.png inside paint if windows pc."""
		img_path = os.path.join(self.dir,"output.png") #same as save_pixmap()
		if windows_pc:
			# print(f"Image Path for Paint Image:\n{img_path}\n")
			os.system(f'mspaint "{img_path}"')
		else:
			print("Apple OS will be added in future build.")
		
	
	def main(self,save_path: str,start: int=0,stop: int=None):
		if stop == None:
			stop = len(self.pdf_obj)
		total_text = ""
		for page in self.pdf_obj.pages(start=start,stop=stop):
			total_text += self.__grab_text(page)

		with open(save_path,'w') as f:
			f.write(total_text)

def test_main():
	"""
	Opens a .pdf and given page numbers and text box will extract NON-OCR text and save into a .txt file
	"""
	input_dir = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\ProjectManagementTools\highlight_extractor\pdf_input"
	input_pdf = r"test_highlight.pdf"
	output_txt = r"output.txt"
	rectangle = (77,381,77+456,381+32)
	path_in = os.path.join(input_dir,input_pdf)
	path_out = os.path.join(input_dir,output_txt)

	###Initialize Text & Save the First Page in as an image for width Extraction
	converter = pdf_to_txt(input_dir,path_in) # instantiate
	converter.update_text_rect(rectangle) # update rectange test
	converter.save_pixmap() # save_pixmap for box dimensions
	converter.view_pixmap(windows_pc = True)

	###Loop Through Pages & Save to One Text File###
	converter.main(path_out,start=0,stop=None) # run extractor, can designate which pages also
def main(rectangle = None,save_dir = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\ProjectManagementTools\highlight_extractor\pdf_input",
	input_pdf = r"test_highlight.pdf",output_txt = r"output.txt",page_start=0,page_stop=None):
	if rectangle == None:
		print("Please find rectange dimensions, and than rerun IF you did not mean to convert the entire page")

	path_in = os.path.join(save_dir,input_pdf)
	path_out = os.path.join(save_dir,output_txt)

	converter = pdf_to_txt(save_dir,path_in,bounding_box=rectangle) # instantiate
	converter.main(path_out,start=page_start,stop=page_stop) # run extractor, can designate which pages also

def find_pixels(save_dir,input_pdf = r"test_highlight.pdf",pixel_page_num = 0):
	path_in = os.path.join(save_dir,input_pdf)

	converter = pdf_to_txt(save_dir,path_in)
	converter.save_pixmap(page_num=pixel_page_num) # save_pixmap for box dimensions
	converter.view_pixmap(windows_pc = True)

if __name__ == '__main__':
	#test runs
	pixels = (77,381,77+456,381+32)
	main(pixels)
	find_pixels(r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\ProjectManagementTools\highlight_extractor\pdf_input")