#Opens .csv file and opens it in pandasGUI
import pandas as pd
from pandasgui import show

def main(csv_path=r"S:\Personal Folders\Databases\Cleaned_Dataset.csv"):
	"""path defaulted to Fastfield Cleaned Dataset Path, but can be changed if needed"""
	data = pd.read_csv(csv_path,index_col=0)
	show(data)

if __name__ == '__main__':
	main()