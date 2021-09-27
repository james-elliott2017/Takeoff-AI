# Main Function for accessing, testing, and running Fastfield Management Scripts
from functions.fastfield_pdf_organizer import main as pdf_org_main
from functions.fastfield_json_reader import raw_json_combiner_main
from functions.fastfield_dataset_cleaner import main as update_clean_dataset

def main():
	UPDATE_CLEAN_DATASET = True
	NEW_FILE_FLAG = pdf_org_main()
	#Update JSON Only if New Dailys Exist --> Replace with EventHandle() in Long Term
	if NEW_FILE_FLAG:
		raw_json_combiner_main()
	if UPDATE_CLEAN_DATASET:
		print("updating clean dataset")
		update_clean_dataset()

if __name__ == '__main__':
	main()