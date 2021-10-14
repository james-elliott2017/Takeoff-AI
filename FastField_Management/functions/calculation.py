#file for scrubbing & analyzing fastfield datasets
import pandas as pd
import os

class load_csv:
	def __init__(self,csv_path):
		self.csv_path = csv_path
		self.dataset = pd.read_csv(csv_path)
class calculations(load_csv):
	def __init__(self,csv_path):
		super().__init__(csv_path)
	def grab_job_rows(self,job_number,job_num_column_name="Job Number"):
		"""return rows of given job_number"""
		job_rows = self.dataset.loc[self.dataset[job_num_column_name] == job_number]
		return job_rows
	def sum(self,job_number,col_to_sum):
		"""sums column based on job number conditional"""
		job_rows = self.grab_job_rows(job_number)
		col_sum = job_rows[col_to_sum].sum()
		return col_sum

def test_main():
	data_path = r"S:\Personal Folders\Databases\Cleaned_Dataset_testing.csv"
	job = 4670
	calcs = calculations(data_path)
	calcs.sum(job,"fiber_terminated")

if __name__ == '__main__':
	test_main()