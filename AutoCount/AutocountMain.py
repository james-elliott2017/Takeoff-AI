# Main
# Top level for visual identifier project

# from opencv_master.modules.python.package import cv2
# import cv2
# import numpy as np
# from matplotlib import pyplot as plt

from pathlib import Path
import os
import pandas as pd
import numpy as np
import cv2
import time
import imutils
from matplotlib import pyplot as plt

###GLOBALS### --- 21 total
					#red	#green		#blue	#pink			#yellow		#dark pink	#dark red	#dark yellow	#torquoise	#light pink		sky blue
template_color = [(0,0,255),(0,255,0),(255,0,0),(255, 157, 214),(0,255,255),(255,0,255),(79, 0, 0),\
		(79, 77, 0),(79, 194, 194),(193, 128, 194),(42, 178, 254),(210,210,0),(210,0,210),(0,210,210)\
		,(150,150,150),(0,150,150),(150,0,150),(150,150,0),(80,0,0),(80,80,80),(80,0,80)]
rotation_list = {90:cv2.ROTATE_90_CLOCKWISE,270:cv2.ROTATE_90_COUNTERCLOCKWISE,180:cv2.ROTATE_180}


def black_filter(image_location,location = False):
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

#Tracker beginning
#COLLECTS A LIST OF FILES TO LOOP THROUGH
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)


    return images

#function converts list to dictionary --> used to remove duplicates
#function called within next function to grab list from tuple
#Used as Final Duplicate Filter
def Convert(lst_x,lst_y):
	it_x = iter(lst_x)
	it_y = iter(lst_y)

	res_dct = dict(zip(it_x, it_y))
	#print("dict =", res_dct)

	x_values = list(res_dct.keys())
	y_values = list(res_dct.values())
	#print(x_values)
	#print(y_values)

	return x_values,y_values
def tuple_seperator(loc):
	if len(loc) != 0:
		x_values = []; y_values = []

		x0 = loc[0]; y0 = loc[1]

		#print(x0)
		x_values= np.append(x_values, x0)
		y_values= np.append(y_values, y0)

		#print("start of combining")
		#print("all x coordinate:", x_combined)

		xy_total = list(Convert(x_values, y_values))

		output = (np.array(xy_total[0], dtype=np.int64), np.array(xy_total[1], dtype=np.int64))
		return output
	else:
		return loc

#############################
#####Visual Count Updater####
#############################

#intersection code --- checks for duplicates so one can get an accurate count
def intersected(bottom_left1, top_right1, bottom_left2, top_right2):
    if top_right1[0] < bottom_left2[0] or bottom_left1[0] > top_right2[0]:
        return 0

    if top_right1[1] < bottom_left2[1] or bottom_left1[1] > top_right2[1]:
        return 0

    return True

def visual_updater(image,loc,squareColor,w,h):
	"""
	updates output highlight/resize & counts for specific angle iteration
	"""
	matches = []
	x = 0
	#used to check for overlap but allows close proximity counts to still happen
	w_division = w/4
	h_division = h/4

	for pt in zip(*loc[::-1]):
		intersection = 0
		for match in matches:
			if intersected(match, (match[0] + w_division, match[1] + h_division), pt, (pt[0] + w_division, pt[1] + h_division)):
				intersection = 1
				break
		if intersection == 0:
			matches.append(pt)
			cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (squareColor), 2) #RED
			x += 1
	return x

def image_rotator_templateMatch(picture, template):
	x_total = []; y_total = []
	x_tmp = []; y_tmp = []

	###########################################
	angle_iteration = 90 #changes how much the picture rotates per rotation
	#^Unless Noted DO NOT Change^#
	threshold = 0.80 #accuracy threshold
	#########################################
	for angle in np.arange(0,360,angle_iteration):
		#print("angle:",angle)
		rotated_template = rotate_image(template, angle)
		#rotated_template = imutils.rotate_bound(template, angle)
		res = cv2.matchTemplate(picture,rotated_template,cv2.TM_CCOEFF_NORMED)
		#Start of Box and Count Coded
		loc = np.where(res >= threshold)
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

	loc_local_symbol = (np.array(x_total, dtype=np.int64), np.array(y_total, dtype=np.int64))
	#print("loc_combined:",loc_local_symbol)
	loc_local_symbol = tuple_seperator(loc_local_symbol)
	#print("loc_filtered:",loc_local_symbol)
	#print("Symbol Complete")
	return loc_local_symbol

def rotate_image(mat, angle):
    """
    Rotates an image via cv2.rotate(mat,dict()) (angle in degrees)
    """
    #print("angle:", angle)
    symbol_rotation = rotation_list.get(angle)
    #print("rotation_list:", symbol_rotation)

    if angle != 0:
    	output = cv2.rotate(mat, symbol_rotation)
    else:
    	output = mat
   
    return output

############################
#######start of code########
############################


def image_count(plans, page_count,project_directory,black_scrub = True):
	"""
	plans,page_count,projDir
	"""
	#COLLECT IMAGES AS LIST
	symbol_picture_directory = project_directory + r"\\" + r"symbol_images"
	folder = os.listdir(symbol_picture_directory)
	#print("folder =", folder)

	final_symbol_counts = []

	###Folder Settings for Saved Highlights### --- Allocation for Multiple Highlighted Pages
	h_count = page_count
	highlightsPath = project_directory + r"\\" + r"highlights_final"
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
				pic = symbol_file + "\\" + picture

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
						tmp_img_gray = black_filter(fileHighlights,location=True)
					else:
						tmp_img_gray = cv2.imread(fileHighlights)
						tmp_img_gray = cv2.cvtColor(tmp_img_gray,cv2.COLOR_BGR2GRAY)

					cv2.imwrite(r".\filter_temp.jpeg", tmp_img_gray) #deleted at end of function
					tmp_img_gray = cv2.imread(r".\filter_temp.jpeg")
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
					loc_local_symbol = image_rotator_templateMatch(resized, template)
					#print("loc_local_symbol:",loc_local_symbol)

					#########################################################################################
					###Seperate functions so that templateMatching, appending/file, and than visual_updates
					###can be done in that order
					#########################################################################################


					squareColor = template_color[list_number]
					x = visual_updater(resized_color, loc_local_symbol, squareColor, w, h)
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

	os.remove(r".\filter_temp.jpeg")
	return final_symbol_counts
#Tracker ending

# initializations
def create_project(project_name):
	"""
	creates project directory and passes project location. 
	NOTE: passes location of existing directory also without overwriting
	"""
	project_folder_names = ["symbol_images","plans_images","highlights_final","TextExtractor_files","Misc_Files"]
	#below directory is where all projects are stored
	primary_directory = (r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\Walker Projects")

	project_directory = primary_directory+ "\\" + project_name
	try:
		os.mkdir(project_directory)

		for folder in project_folder_names:
			sub_folder = project_directory + "\\" + folder
			os.mkdir(sub_folder)

		#Create __init__ file for project access for text search/OCR/text_extraction library
		init = project_directory + r"\\" + project_folder_names[3]\
			+ r"\\" + r"__init__.py" #TextExtractor_files location
		#print(init)
		open(init,'a').close()
	except:
		print("folder already exists")

	finally:
		return project_directory

def csv_write(my_dict,header,project_folder):
	if project_folder:
		save_location = project_folder + r"\\" + "project_counts.csv"
		(pd.DataFrame.from_dict(data=my_dict, orient='index')
		   .to_csv(save_location, header=header))
	else:
		(pd.DataFrame.from_dict(data=my_dict, orient='index')
		   .to_csv(header=header))

def search_multiple_pages(plans_file_names,plans_folder,projDir):

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
		page_total = image_count(plans, page_count,projDir,black_scrub=False)
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

###########################
# Start of Executable Code#
###########################
#access project & create new projects if already existing

def run_counts(project_name):
    projDir = create_project(project_name)

    plans_folder = projDir + r"\\" + r"plans_images"
    plansFiles = os.listdir(plans_folder)

    output = search_multiple_pages(plansFiles,plans_folder,projDir)

    symbol_picture_directory = projDir + r"\\" + r".\symbol_images"
    symbol_names = os.listdir(symbol_picture_directory)

    print("symbol_names:", symbol_names)
    print("output:",output)
    #SAVE COUNTS AS .CSV FILE
    csv_write(output, symbol_names,projDir)

#Comment if using GUI
if __name__ == "__main__":
	project = "TEST" # INPUT PROJECT NAME HERE
	run_counts(project)
#########################
#####TO DO LIST##########
#########################

#1) counter to break out of Loop if Max count has already been found (speeds up calculations)

#3) update template matching functions to allow order of sequences described in tracker.py

#4) Change Folder names inside tracker to list[locations] based on folder_names list, so we don't have to change everything when folder name changes

#create crop so that image can shrink too correct size
#Manually decide where in an image to search, will save time
