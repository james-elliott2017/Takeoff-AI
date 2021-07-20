#watermarking Logos & Hiding logos based on pdf location
from PIL import Image
import fitz
import os

class watermark():
	def __init__(self):
		self.input_pdf = r"example_files/test_page.pdf"
		self.output_pdf = r'output_folder/output_pdf.pdf'
		vert_img, horz_img = (r"logos/walker_full_rotated.png",r"logos/walker_full_logo.png")
		self.img_logo = vert_img
		self.config_img = r"output_folder/config_img.png"

		self._instance_info(config_img=True)

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

if __name__ == '__main__':
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