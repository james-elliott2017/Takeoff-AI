#watermarking Logos & Hiding logos based on pdf location
from PIL import Image, ImageTk
import fitz
import os

class watermark():
	def __init__(self,img_type=0):
		"""img_type: 0 = Horzontal, 1 = vertical"""
		self.update_dir()
		if img_type == 0:
			self.img_logo = self.horz_img
		else:
			self.img_logo = self.vert_img

		# self._instance_info(config_img=True)


	def update_dir(self,new_working_dir=""):
		"""appends references for input/output files with new dir"""
		self.new_working_dir = new_working_dir
		print(new_working_dir)
		self.input_pdf = os.path.join(new_working_dir,r"example_files/test_page.pdf")
		self.output_pdf = os.path.join(new_working_dir,r'output_folder/output_pdf.pdf')
		self.vert_img = os.path.join(new_working_dir,r"logos/walker_full_rotated.png")
		self.horz_img = os.path.join(new_working_dir,r"logos/walker_full_logo.png")
		self.config_img = os.path.join(new_working_dir,r"output_folder/config_img.png")

	def update_img_logo(self):
		"""Used to change img_logo between vertical and horizontal formats"""
		pass

	def get_img_dims(self,img_path):
		tmp = Image.open(img_path)
		w,h = tmp.size
		return (w,h)

	def print_pdf_page_dims(self,pdf_source,save_png = False):
		document = fitz.open(pdf_source)
		pix_map = document.getPagePixmap(0)
		dims = pix_map.irect

		if save_png == True:
			pix_map.save(self.config_img)

		return dims

	def add_img(self,logo_box,wb=None):
		"""
		logo_box: fitz.Rect() object
		wb: fitz.Rect() object
		"""
		document = fitz.open(self.input_pdf)
		new_doc = fitz.open() #new_file to work with

		# We'll put image on first page only but you could put it elsewhere
		logo_px = fitz.Pixmap(self.img_logo)
		for i in range(document.page_count):
			px_page = document.getPagePixmap(i)

			#insert white box
			if wb != None:
				px_page.clear_with(255,wb)

			new_doc.insert_page(-1,width=px_page.width,height=px_page.height)
			new_doc[i].insert_image(px_page.irect,pixmap=px_page)

			#insert logo
			new_doc[i].insert_image(logo_box, pixmap=logo_px,keep_proportion=False)
			new_doc.save(self.output_pdf,garbage=4,deflate=True)
			print(f"Page {i} Complete")

		document.close()
		new_doc.close()

	def _instance_info(self,config_img = False):
		"""
		print helper function
		"""
		w,h = self.get_img_dims(self.img_logo)
		pdf_dims = self.print_pdf_page_dims(self.input_pdf,save_png=config_img)
		print("Instance has")
		print("Logo Size w: {},h: {}".format(w,h))
		print("PDF ~DIM: {}\n".format(pdf_dims))

	def pixmap_preview(self):
		"""
		Preview the Watermark of the first page, returns image file location

		logo_box: fitz.Rect() object
		wb: fitz.Rect() object
		"""
		document = fitz.open(self.input_pdf)
		preview_pixmap = document.getPagePixmap(0)
		file_loc = os.path.join(self.new_working_dir,"tmp_img.gif")
		preview_pixmap.save(file_loc)
		document.close()
		return file_loc


	def _horizontal_bot_center_dim(self):
		"""
		uses pixmap() references to decide where to put an image
		"""
		pass
	def _vertical_right_center_dim(self):
		"""
		uses pixmap() reference to decide where to put vertical image
		"""
		pass

def test_func():
	watermark_class = watermark()
	
	#USE MS PAINT FOR PIXEL LOCATIONS
	x,y = (2705,329) ##LOGO POSITION (top left corner)
	w,h = watermark_class.get_img_dims(watermark_class.img_logo)
	w,h = (219,1045)
	#whiteout area on left
	wht_x,wht_y = (2665,293) #top_left corner
	white_size = (317,1147)

	white_box = fitz.Rect(wht_x,wht_y,wht_x+white_size[0],wht_y+white_size[1])
	logo_box = fitz.Rect(x,y,x+w,y+h)
	
	watermark_class.add_img(logo_box,wb=white_box)
	print("Walker Insert Complete")
def watermark_main(input_pdf):
	wMark = watermark(img_type=1) #0 for horizontal, 1 for vertical
	#USE MS PAINT FOR PIXEL LOCATIONS
	x,y = (2750,280) ##LOGO POSITION (top left corner)
	w,h = wMark.get_img_dims(wMark.img_logo)
	w,h = (219,975)
	#whiteout area on left
	wht_x,wht_y = (2675,275) #top_left corner
	white_size = (450,1050)

	white_box = fitz.Rect(wht_x,wht_y,wht_x+white_size[0],wht_y+white_size[1])
	logo_box = fitz.Rect(x,y,x+w,y+h)

	#Input Input Pdf Location
	wMark.input_pdf = input_pdf
	
	wMark.add_img(logo_box,wb=white_box)
	print("Walker Insert Complete")

if __name__ == '__main__':
	input_pdf = r"S:\Shared Folders\Steven\Quotes\5600\5669 - SCVMC Technology Pachage - Fiber Infrastructure\Drawings & Specs\C) Drawings\Walker - Bid Set Design Edits (James).pdf"
	watermark_main(input_pdf)