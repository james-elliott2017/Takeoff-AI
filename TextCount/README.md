# OCR Package
## Goals:  
The purpose of our OCR is 2 fold:  
  1. Allow easy-of-use when transfering OCR Data from construction plans into Excel format  
  2. Allow counting to be done via words or letters. (Beta Version --> Works with TextExtractMain) --> Sometimes faster and easier than TemplateMatching Approach  
## Current State:  
TextExtract Main can take in key words & .txt files created from PDF-Construction Drawings to count how many times a KEY word or phrase appears. This is than organized into project folders based on the names your provide in Takeoff_Main.py. 

## Setup:  
If you are planning to use the software on your local computer. Please follow the steps below.
1. Download the repo locally. You can decide where you want to put it, but remember that the library is local to that repo unless you manually add it to your pythons global packages.  
2. Go into TextExtractorMain & AutocountMain. You will see the instantiation of the respective class. Make sure to change the HARD paths to match where you installed the package.
3. Go to "Takeoff_Main.py" and run this file. You can add argsvarse() if you prefer command line, but in its given state I edit and than call the script.
4. You can comment and uncomment the text extractor and AutoCount functions based on what feature you are using.

## Demo:
_Coming Soon_
