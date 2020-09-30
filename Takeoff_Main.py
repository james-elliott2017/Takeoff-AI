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
project = r"6082 Sunnyville Civic Center"
division = r"LowVoltage"


###TEXT EXTRACTOR###
textExtracMain(project, division)

###AutoCount###
#run_counts(project)


###OCR###