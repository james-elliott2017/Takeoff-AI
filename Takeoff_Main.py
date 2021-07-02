#James Elliott
#9/18/2020

#Primary Script to all projects
#FINAL VERSION --- put all calls here so that javascript can communicate with this file

import os
import sys
import re

from OCRLibrary.TextExtractorMain import textExtracMain
from AutoCount.AutocountMain import run_counts


#FINAL VERSION --- one script for autocount & text_count --> allows shared project name
project = r"5637_Madesto_Courthouse"

#current version only works with text_counting
division = r"Data_Floor"

###AutoCount###
#Must run first for new projects--> run_counts(project)#

run_counts(project)

###TEXT EXTRACTOR###

#textExtracMain(project, division)


###OCR###


###TO DO LIST###
#1. Convert AutoCountMain into a singular class (AutoMainCount)
#2 Add image_search_dimensions for cropping out edges (AutoMainCount)
#3 Add text window to ignore edges (TextExtractormain)
#4 add in ' # ', so you can find only numbers that are by themselves (TextExtractormain)
#5 Change CSV formatting to use highlight name instead