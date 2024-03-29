# AutoCount Main 2.0
# __version__ == 2.0:
# 1) Organized in class structure for ease of use
# 2) Added windowing feature for AutoCount if wanted.
#	Allows a portion of images to be searched over, instead of the complete thing
import os
import pandas as pd
import numpy as np
import cv2
import time
import imutils
import json
from typing import List, Dict,Iterator,Tuple,Union

#test imports only
## import icecream as ic

class create_default_json:
	def __init__(self,save_dir: str,file_name: str ="Constants.json"):
		"""helper class for img_count.create_project()"""
		self.json_dict = {
			"default":["search_1","search_2"]
		}
		self.__create_json(save_dir,name=file_name)
	def __create_json(self,save_dir,name="Constants.json"):
		complete_path = os.path.join(save_dir,name)
		with open(complete_path,'w') as f:
			json.dump(self.json_dict,f)

class img_count:
	def __init__(self,projects_dir: str =r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\Walker Projects"):
		self.template_color:Iterator[Tuple[int,int,int]] = [(0,0,255),(0,255,0),(255,0,0),(255, 157, 214),(0,255,255),
			(255,0,255),(79, 0, 0),(79, 77, 0),(79, 194, 194),(193, 128, 194),\
			(42, 178, 254),(210,210,0),(210,0,210),(0,210,210)\
		,(150,150,150),(0,150,150),(150,0,150),(150,150,0),(80,0,0),(80,80,80),(80,0,80)]
		self.rotation_list = {90:cv2.ROTATE_90_CLOCKWISE,270:cv2.ROTATE_90_COUNTERCLOCKWISE,180:cv2.ROTATE_180}

		#Initialization Code for Creating New Projects & Accessing Old Projects -->create_project()
		self.project_folder_names = ["symbol_images","plans_images","highlights_final","TextExtractor_files","Misc_Files"]
		self.primary_directory = projects_dir
		self.symbol_sub_folder = r"symbol_images"
		self.imgs_with_highlights_sub_folder = r"highlights_final"

		#Matching Variables CAN be changed if you wish
		self.angle_iteration = 90
		self.threshold = 0.80
	def __black_filter(self, image_location: str,location:bool = False):
		"""
		input: image
		Removes all other colors except for a black threshold
		make location = True if your input is a file & not a array!!!
		"""
		#open image
		if location == True:
			drawing = cv2.imread(image_location)
		else:
			drawing = image_location


		picture = cv2.cvtColor(drawing, cv2.COLOR_BGR2HSV)
		
		#filter out colors except for dark black
		lower_black = np.array([0,0,0])
		upper_black = np.array([360,20,90])

		mask = cv2.inRange(picture, lower_black, upper_black)
		final_image =cv2.bitwise_not(mask)

		return final_image
	def __load_images_from_folder(self, folder: str):
		images = []
		for filename in os.listdir(folder):
			img = cv2.imread(os.path.join(folder,filename))
			if img is not None:
				images.append(img)
		return images
	def __Convert(self,lst_x: List[int],lst_y:List[int]) -> Tuple[List[int],List[int]]:
		it_x = iter(lst_x)
		it_y = iter(lst_y)

		res_dct = dict(zip(it_x, it_y))
		#print("dict =", res_dct)

		x_values = list(res_dct.keys())
		y_values = list(res_dct.values())
		return (x_values,y_values)
	def __tuple_seperator(self,loc: Tuple[np.ndarray,np.ndarray]) -> Union[int,np.array]:
		"""
		loc: tuple of 2 ndarrays() for x,y coordinates
		"""
		if len(loc) != 0:
			xy_total = self.__Convert(loc[0], loc[1])

			output = np.array(xy_total[0], dtype=np.int64), np.array(xy_total[1], dtype=np.int64)
			return output
		else:
			return loc
		#intersection code --- checks for duplicates so one can get an accurate count
	def __intersected(self,bottom_left1:int, top_right1:int, bottom_left2:int, top_right2:int):
		if top_right1[0] < bottom_left2[0] or bottom_left1[0] > top_right2[0]:
			return 0

		if top_right1[1] < bottom_left2[1] or bottom_left1[1] > top_right2[1]:
			return 0
		return True

	def __visual_updater(self,image: np.ndarray,loc:np.ndarray,squareColor:Tuple[int,int,int],w:int,h:int) -> int:
		"""
		Updates Counts based on different iterations of a resized counter-object. Makes sure that 2 images do not intersersect.
		Inputs: Image_1 & Found Objects Location for Intersection check, Color of Square marking for output_highlights if new object.
		Output: Count of None-Intersecting Objects
		"""
		matches = []
		x = 0
		#used to check for overlap but allows close proximity counts to still happen
		w_division = w/4
		h_division = h/4

		for pt in zip(*loc[::-1]):
			intersection = 0
			for match in matches:
				if self.__intersected(match, (match[0] + w_division, match[1] + h_division), pt, (pt[0] + w_division, pt[1] + h_division)):
					intersection = 1
					break
			if intersection == 0:
				matches.append(pt)
				cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (squareColor), 2) #RED
				x += 1
		return x

	def __image_rotator_templateMatch(self,picture:np.ndarray, template:np.ndarray):
		"""Takes original image & template and runs a convolution of the two and returns percentage of match."""
		x_total = []; y_total = []
		x_tmp = []; y_tmp = []

		#matches given THRESHOLD & ANGLE. REDUCE ANGLE FOR SPEED INCREASE
		for angle in np.arange(0,360,self.angle_iteration):
			#print("angle:",angle)
			rotated_template = self.__rotate_image(template, angle)
			res = cv2.matchTemplate(picture,rotated_template,cv2.TM_CCOEFF_NORMED)
			#Start of Box and Count Coded
			loc = np.where(res >= self.threshold)
			#code to print image
			#print("loc =", loc)

			#loop to add more locations if search found some --- filter is applied later
			if len(loc[0]) != 0:
				x_tmp.append(loc[0])
				y_tmp.append(loc[1])
				x_total = np.concatenate((x_tmp[0], x_total))
				y_total = np.concatenate((y_tmp[0], y_total))
				x_tmp = []; y_tmp = []
		#End of For Loop, combines rotated symbol matches together and filters duplicates
		# Organize Found Matches that meet Threshold
		loc_local_symbol = (np.array(x_total, dtype=np.int64), np.array(y_total, dtype=np.int64))
		loc_local_symbol = self.__tuple_seperator(loc_local_symbol)
		return loc_local_symbol
	def __rotate_image(self,mat:np.ndarray, angle: Dict[int,int])-> np.ndarray:
		"""
		Rotates an image via cv2.rotate(mat,dict()) (angle in degrees)
		"""
		symbol_rotation = self.rotation_list.get(angle)
		if angle != 0:
			output = cv2.rotate(mat, symbol_rotation)
		else:
			output = mat
		return output

	#Main Loop ---> Needs to be cleaned, and possibly seperated into another Class and than inherited.
	def __image_count(self,plans:str, page_count:int,black_scrub:bool = True) -> List[int]:
		"""
		plans (.png path),page_count (int),projDir (string path)
		Output: A single Pages Counts as a List. ALL Symbols
		"""
		temp_img_file = r".\filter_temp.png" #temp file saved between loops
		#COLLECT IMAGES AS LIST
		symbol_picture_directory = os.path.join(self.projDir,self.symbol_sub_folder)
		folder = os.listdir(symbol_picture_directory)
		#print("folder =", folder)

		final_symbol_counts = []

		###Folder Settings for Saved Highlights### --- Allocation for Multiple Highlighted Pages
		h_count = page_count
		highlightsPath = os.path.join(self.projDir,self.imgs_with_highlights_sub_folder)
		highlights = 'highlights' + "_" + str(h_count) + ".jpg"
		fileHighlights = os.path.join(highlightsPath ,highlights)

		temp_img = cv2.imread(plans)
		cv2.imwrite(fileHighlights,temp_img)
		################################
		list_number = 0
		#folder_length = len(folder) - 1 #account for zero starting point
		for sym in folder:
			#print("length",folder_length)
			symbol_file = symbol_picture_directory + "\\" + sym
			#print(os.listdir(symbol_file))
			#print("sym:", sym)
			symbol_counts = [] #local_folder symbol counts, combined and reset per folder
			count = 0 #counts for iterations of symbols in folder
			number_of_symbols = len(os.listdir(symbol_file)) - 1
			#loops through all symbols in given folder IF folder isn't empty
			if len(os.listdir(symbol_file)) != 0:
				for picture in os.listdir(symbol_file):

					#START OF TEMPLATE MATCHING CODE#
					pic = os.path.join(symbol_file,picture)

					template = cv2.imread(pic)
					template = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)

					#template = cv2.Canny(template,50,200)
					w, h = template.shape[::-1]

				#cv2.imshow("Template",template)
				#cv2.waitKey()
					print("Starting matchTemplate Loop")
					best_counts = 0

					#Loop over scales of image
					scale_loop = 2 #Used to give number of iterations and to append list at end of function
					lowest_scale = .5 #used for smallest resize & to test if loop is on final iteration <-- workes because looping in reverse
					for scale in np.linspace(lowest_scale, 1.0,scale_loop)[::-1]:

						img_rgb = cv2.imread(fileHighlights)

						if black_scrub == True:
							tmp_img_gray = self.__black_filter(fileHighlights,location=True)
						else:
							tmp_img_gray = cv2.imread(fileHighlights)
							tmp_img_gray = cv2.cvtColor(tmp_img_gray,cv2.COLOR_BGR2GRAY)

						cv2.imwrite(temp_img_file, tmp_img_gray) #deleted at end of function
						tmp_img_gray = cv2.imread(temp_img_file)
						img_gray = cv2.cvtColor(tmp_img_gray, cv2.COLOR_BGR2GRAY)
							#OLD VERSION PRE BLACK FILTER#####################################################
						#img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
						#img_gray = cv2.Canny(img_gray,50,200)


						resized_color = imutils.resize(img_rgb, width = int(img_gray.shape[1] * scale))
						resized = imutils.resize(img_gray, width = int(img_gray.shape[1] * scale))
						#if statements breaks out if main image becomes smaller than searching image "should NEVER happen with drawings"
						if resized.shape[0] < h or resized.shape[1] < w:
							break
						
						#rotational templateMatch with copy filter OUTPUT = identified images
						loc_local_symbol = self.__image_rotator_templateMatch(resized, template)
						#print("loc_local_symbol:",loc_local_symbol)

						#########################################################################################
						###Seperate functions so that templateMatching, appending/file, and than visual_updates
						###can be done in that order
						#########################################################################################

						squareColor = self.template_color[list_number]
						x = self.__visual_updater(resized_color, loc_local_symbol, squareColor, w, h)
						total = x

						#Updates Output PNG if better count found
						if total > best_counts:
							final_image = resized_color
							time.sleep(.01) #pause for 1 milli second

						#updates to keep best_counts/image searched
						if best_counts == 0 or total > best_counts:
							best_counts = total


						print("loop total =",total)
						#Runs on final scaling loop
						if scale == lowest_scale:
							symbol_counts.append(best_counts)

						if scale == lowest_scale and best_counts != 0:
							cv2.imwrite(fileHighlights,final_image)
							print("highlights updated")

					if count == number_of_symbols:
						final_symbol_counts.append(sum(symbol_counts))
						print("total_per_symbol:",final_symbol_counts)
					count += 1
					#print("count:",count)
					#print(sym)
			else:
				print("folder is empty")
				best_counts = 0
				final_symbol_counts.append(best_counts)

			list_number = list_number + 1
			print(" ")
			print("local_max = ", best_counts)
			print("folder =", symbol_file)

		os.remove(temp_img_file)
		return final_symbol_counts

	def __search_multiple_pages(self,plans_file_names:Iterator[str],plans_folder:str)-> Dict[str,int]:
		"""
		Wrapper to allow page counts to work with just directory and img file names.
		Output: dict("Page Name", int(total counts for each symbol)
		"""
		d = dict()
		page_count = 0
		final_counts = []
		for pics in plans_file_names:
			plans = plans_folder + "\\" + pics

			###Progress Bar Code###
			max_pages = len(plans_file_names)
			percentage = round((float(page_count)/max_pages) * 100,2)
			tmp = "Current Progress Is {}%".format(percentage)
			print(percentage)
			print(tmp)	


			##############################################################################################
			page_total = self.__image_count(plans, page_count,black_scrub=False)
			print("page_total =", page_total)

			final_counts.append(page_total)
			print("final_counts =", final_counts)

			# Code to create dictionary connection for each sheet will be extraced later by another function

			d[pics] = final_counts[page_count]
			CountsPerPage = d
			print(CountsPerPage)

			# adds page number for next cycle
			page_count += 1
		return d

######initializations --- USER CALLED FUNCTIONS#########################
	def create_project(self,project_name):
		"""
		creates project directory and passes project location. 
		NOTE: passes location of existing directory also without overwriting
		"""

		project_directory = self.primary_directory+ "\\" + project_name
		try:
			os.mkdir(project_directory)

			for folder in self.project_folder_names:
				sub_folder = project_directory + "\\" + folder
				os.mkdir(sub_folder)

			#Create __init__ file for project access for text search/OCR/text_extraction library
			init = project_directory + r"\\" + self.project_folder_names[3]\
				+ r"\\" + r"__init__.py" #TextExtractor_files location
			#print(init)
			open(init,'a').close()

			#create json for textCount()
			sub_folder = "TextExtractor_files"
			complete_dir_path = os.path.join(project_directory,sub_folder)
			create_default_json(complete_dir_path,file_name='Constants.json')
			print(f"{project_name} Created")
		except:
			print("folder already exists")

		finally:
			return project_directory

	def csv_write(self,my_dict,header,project_folder):
		if project_folder:
			save_location = project_folder + r"\\" + "project_counts.csv"
			(pd.DataFrame.from_dict(data=my_dict, orient='index')
			   .to_csv(save_location, header=header))
		else:
			(pd.DataFrame.from_dict(data=my_dict, orient='index')
			   .to_csv(header=header))
	def run_counts(self, projDir:str,is_dir:bool = True) -> None:
		"""
		Should follow directly after create_project
		projDir: output of create_project, input will be passed directly into create_project
		"""
		if is_dir == False:
			projDir = self.create_project(projDir)
		self.projDir = projDir #Directory Name with Project Number in Path

		plans_folder = os.path.join(self.projDir,r"plans_images")
		plansFiles = os.listdir(plans_folder)

		output = self.__search_multiple_pages(plansFiles,plans_folder)

		symbol_picture_directory = os.path.join(self.projDir,self.symbol_sub_folder)
		symbol_names = os.listdir(symbol_picture_directory)

		print("symbol_names:", symbol_names)
		print("output:",output)
		#SAVE COUNTS AS .CSV FILE
		self.csv_write(output, symbol_names,self.projDir)


if __name__ == "__main__":
	test_class = count()
	print(test_class.self.template_color)

