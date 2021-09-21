# Main Function for accessing, testing, and running Fastfield Management Scripts
from functions.fastfield_pdf_organizer import main as pdf_org_main
from functions.fastfield_json_reader import raw_json_combiner_main

def main():
	NEW_FILE_FLAG = pdf_org_main()
	#Update JSON Only if New Dailys Exist --> Replace with EventHandle() in Long Term
	if NEW_FILE_FLAG:
		raw_json_combiner_main()
if __name__ == '__main__':
	main()