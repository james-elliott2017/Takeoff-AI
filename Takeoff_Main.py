#James Elliott
#9/18/2020
#__version__ == '2.0'
#Primary Script to all projects
#FINAL VERSION --- put all calls here so that javascript can communicate with this file

from AutoCount.AutocountMain import count
from OCRLibrary.TextExtractorMain import text_counter

project = r"5638_NAVFAC"
division = r"Data_Floor" #text_extractor ONLY

###LOAD PROJECT###
AutoCount_Class = count()
working_dir = AutoCount_Class.create_project(project) #works as a loader also

###AutoCount###
# AutoCount_Class.run_counts(working_dir,is_dir=True)

###TEXT EXTRACTOR###
text_class = text_counter()
text_class.textExtracMain(project, division)

###OCR-Extractor###
# coming soon

###TO DO LIST###
#2 Add image_search_dimensions for cropping out edges (AutoMainCount)
#3 Add text window to ignore edges (TextExtractormain)
#5 Change CSV formatting to use highlight name instead