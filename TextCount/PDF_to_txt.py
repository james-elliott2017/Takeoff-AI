import os
import fitz

class pdf_to_txt():
	def __init__(self,directory: str,pdf_location: str,bounding_box = None):
		self.dir = directory
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
	def save_pixmap(self):
		pixmap = self.pdf_obj[0].get_pixmap()
		pixmap.save(os.path.join(self.dir,"output.png"))
	def open_pixmap(self):
		"""opens pixmap output.png inside paint if windows pc."""
		pass
	
	def main(self,save_path: str,start: int=0,stop: int=None):
		if stop == None:
			stop = len(self.pdf_obj)
		total_text = ""
		for page in self.pdf_obj.pages(start=start,stop=stop):
			total_text += self.__grab_text(page)

		with open(save_path,'w') as f:
			f.write(total_text)
	def img_helper(self):
		"""Takes first page of image, and saves in working directory"""
		pass

def main():
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

	###Loop Through Pages & Save to One Text File###
	converter.main(path_out,start=0,stop=None) # run extractor, can designate which pages also

if __name__ == '__main__':
	main()