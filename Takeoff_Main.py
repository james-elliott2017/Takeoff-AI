#James Elliott
#9/18/2020
#__version__ == '2.0'
#Primary Script to all projects
#FINAL VERSION --- put all calls here so that javascript can communicate with this file

from OCRLibrary.TextExtractorMain import textExtracMain
from AutoCount.AutocountMain import count
from OCRLibrary.TextExtractorMain_Beta import text_counter


#FINAL VERSION --- one script for autocount & text_count --> allows shared project name
project = r"5638_NAVFAC"

#current version only works with text_counting
division = r"Data_Floor"

###LOAD PROJECT###
AutoCount_Class = count()
working_dir = AutoCount_Class.create_project(project)

###AutoCount###
#AutoCount_Class.run_counts(working_dir,is_dir=True)

###TEXT EXTRACTOR###
#textExtracMain(project, division)
text_class = text_counter()
text_class.textExtracMain(project, division)

###OCR###
#not existing yet

###TO DO LIST###
#2 Add image_search_dimensions for cropping out edges (AutoMainCount)
#3 Add text window to ignore edges (TextExtractormain)
#4 Class(ify) textExtracMain()
#5 Change CSV formatting to use highlight name instead