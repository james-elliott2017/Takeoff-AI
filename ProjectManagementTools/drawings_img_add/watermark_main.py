#watermarking Logos & Hiding logos based on pdf location
from PIL import Image
import fitz
import os
from numpy import zeros
import numpy as np

src_pdf_filename = "Telecomm_Walker.pdf"


dst_pdf_filename = 'output_pdf.pdf'
img_logo = "walker_full_logo.png"
img_white = "white_space.png"

print("Imports Complete")

def get_img_dims(img_path):
	tmp = Image.open(img_path)
	w,h = tmp.size
	return (w,h)

def create_white_canvas(x,y):
	imga = zeros([y,x,3])
	h = len(imga)
	w = len(imga[0])

	for y in range(h):
	    for x in range(w):
	        imga[y,x] = [255,255,255] #COLOR OF BOX

	img = Image.fromarray(imga.astype(np.uint8))
	img.save("white_space.png")

def add_img(x,y,w,h,img_filename,whiteout=False,wr=[]):
	"""
	wr: 'white_rect = [top_left_x,top_left_y,bot_right_x,bot_right_y'
	"""
	document = fitz.open(src_pdf_filename)
	new_doc = fitz.open() #new_file to work with

	# We'll put image on first page only but you could put it elsewhere
	logo_px = fitz.Pixmap(img_logo)
	for i in range(document.page_count):
		page = document[i]
		
		if whiteout == True:
			white_rect = fitz.Rect(wr[0], wr[1],wr[2],wr[3])

			px_page = document.getPagePixmap(i)
			px_page.clear_with(255,white_rect)
			print("page size: {}".format(px_page.irect))
			new_doc.insert_page(-1,width=px_page.width,height=px_page.height)
			new_doc[i].insert_image(px_page.irect,pixmap=px_page)
			#1) clear with handles background, so colored square needs to be removed
			#2) organize so we clear and append logo
			#3) Remove create square call as well
			#4) Edit input dimension to fit new scan
		# Set position and size according to your needs
		img_rect = fitz.Rect(x, y, w, h)
		# print(new_doc[i].rect)
		new_doc[i].insert_image(img_rect, pixmap=logo_px,keep_proportion=False)

		new_doc.save("walker_roster.pdf",garbage=4,deflate=True)
	document.close()
	new_doc.close()

if __name__ == '__main__':
	#grab dimensions & ratio
	w,h = get_img_dims(img_logo)
	print("img; w: {},h: {}".format(w,h))

	#whiteout area on left
	white_size = (2150,175)
	
	wht_x,wht_y = (620,2380) #top_left corner
	white_area = (wht_x,wht_y,wht_x+white_size[0],wht_y+white_size[1])
	create_white_canvas(white_size[0], white_size[1])

	#LOGO POSITION
	# pdf tradition page size (595,842)--> (cols,rows)
	x,y = (1200,2350) #top_left image add location
	add_img(x,y,x+w,y+h,img_logo,whiteout=True,wr=white_area)
	print("Walker Insert Complete")

### ISSUES ###
#1) white_canvas DOES not work in current state
#2) weird issue where images don't show on some documents