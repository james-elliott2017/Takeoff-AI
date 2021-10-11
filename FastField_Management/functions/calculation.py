#file for scrubbing & analyzing fastfield datasets
import pandas as pd
import os

class view_csv:
	def __init__(self,csv_path):
		dataset = pd.read_csv(csv_path)
	def view_data(self):
		pass

def test_main():
	data_path = r"S:\Personal Folders\Databases\Cleaned_Dataset.csv"

if __name__ == '__main__':
	main()