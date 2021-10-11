#James Elliott
#9/18/2020
#__version__ == '2.0'
#Primary Script to all projects
#FINAL VERSION --- put all calls here so that javascript can communicate with this file

from AutoCount.AutocountMain import img_count
from TextCount.TextExtractorMain import text_counter

project = r"5645 SCVMC 115 ACD Basement"
# division = r"Data_Floor" #text_extractor ONLY

TEXT_FLAG = False
AUTO_FLAG = True
PDF_TO_TEXT_FLAG = False

###LOAD PROJECT###
AutoCount_Class = img_count(projects_dir=r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\Walker Projects")
working_dir = AutoCount_Class.create_project(project) #works as a loader also

if AUTO_FLAG:
	###AutoCount###
	AutoCount_Class.threshold = 0.85
	AutoCount_Class.run_counts(working_dir,is_dir=True)

###TEXT EXTRACTOR###
if TEXT_FLAG:
	#PDF_to_text --> save to output location
	text_class = text_counter()
	text_class.main_V2_allDivisions(project)

###OCR-Extractor###
# coming soon

###TO DO LIST###
#2 Add image_search_dimensions for cropping out edges (AutoMainCount)
#3 Add text window to ignore edges (TextExtractormain)
#5 Change CSV formatting to use highlight name instead


#DEAL WITH CREATION ERRORS WHEN CREATING NEW JOB