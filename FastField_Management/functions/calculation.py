#file for scrubbing & analyzing fastfield datasets
import pandas as pd
from typing import Union,Tuple
class load_csv:
	def __init__(self,csv_path):
		self.csv_path = csv_path
		self.dataset = pd.read_csv(csv_path)
class pd_single_column:
	def __init__(self,dataset: pd.DataFrame,non_zeros: bool = True) -> None:
		"""non_zeros: parameter True implies summing will ignore columns that don't have a value > 0.
		Set to False if you want all columns to sum no matter what. Can also be updated on case by case basis after initialization.
		"""
		self.dataset = dataset
		self.non_zeros = non_zeros
	def get_mask(self,col_to_mask: str,condition: Union[int,float] = 0):
		"""returns a mask of the given column based on numeric condition"""
		mask = self.dataset[col_to_mask] > condition
		return mask
	def sum_column(self,col_name: str,col_mask: pd.DataFrame = None) -> Union[float,int]:
		"""col_mask ONLY used if non_zeroes == True. Gives mask for summing."""
		if self.non_zeros:
			sum = self.dataset.loc[col_mask,col_name].sum()
			return sum
		sum = self.dataset[col_name].sum()
		return sum		
	def avg_column(self,col_name: str) -> float:
		sum = self.sum_column(col_name)
		col_len = len(self.dataset[col_name])
		average = float(sum/col_len)
		return average
class pd_multi_column(pd_single_column):
	def __init__(self, dataset: pd.DataFrame,non_zeros: bool = True) -> None:
	    super().__init__(dataset,non_zeros=non_zeros)
	def superdivide(self,col_1_name,col_2_name) -> Union[float,int]:
		"""Takes 2 Columns. Sums them. ANd than divides column 1 by column 2
		non_zeros applies a mask is given based on col_1_name, where the value is greater than zero"""
		if self.non_zeros:
			mask = self.get_mask(col_1_name,condition=0)
			sum_1 = self.sum_column(col_1_name,col_mask=mask) #numerator
			sum_2 = self.sum_column(col_2_name,col_mask=mask) #denominator; mask based on numerator ONLY
		else:
			sum_1 = self.sum_column(col_1_name) #numerator
			sum_2 = self.sum_column(col_2_name) #denominator
		final = sum_1/sum_2
		return final
	def multiple_superdivide(self,col_1_list: Union[list,tuple],col_2_name: str) -> Tuple[dict,str]:
		"""wrapper of superdivide where multiple columns can get divided by the same column to produce data."""
		averages = {}
		for col_name in col_1_list:
			averages[col_name] = self.superdivide(col_name,col_2_name)
		units = "Units = Type/Hour"
		return (averages,units)

class calculations(load_csv):#job number specific
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