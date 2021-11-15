#file for scrubbing & analyzing fastfield datasets
import pandas as pd
from typing import Union,Tuple
from copy import deepcopy

class pd_single_column:
	def __init__(self,dataset: pd.DataFrame,non_zeros: bool = True) -> None:
		"""non_zeros: parameter True implies summing will ignore columns that don't have a value > 0.
		Set to False if you want all columns to sum no matter what. Can also be updated on case by case basis after initialization.
		"""
		self.dataset = dataset.fillna(0)
		self.non_zeros = non_zeros

		#Column Defaults for ease-of-use
		self.job_num_col_name = "Job Number"
		self.job_name_col_name = "Project Name"
	def get_mask(self,col_to_mask: str,condition: Union[int,float] = 0):
		"""returns a mask of the given column based on numeric condition"""
		mask = self.dataset[col_to_mask] > condition
		return mask
	def sum_column(self,col_name: str,col_mask: pd.DataFrame = None,new_dataset: pd.DataFrame = None) -> Union[float,int]:
		"""col_mask ONLY used if non_zeroes == True. Gives mask for summing.
		new_dataset: If used must already be masked. Or in other words, is only going to be summed.
		"""
		if type(new_dataset) == type(None):
			if self.non_zeros:
				sum = self.dataset.loc[col_mask,col_name].sum()
				return sum
			sum = self.dataset[col_name].sum()
		else:
			#used if you want to pass a new dataset instead of the classes base dataset. Only sums
			sum = new_dataset[col_name].sum()
		return sum		
	def avg_column(self,col_name: str) -> float:
		sum = self.sum_column(col_name)
		col_len = len(self.dataset[col_name])
		average = float(sum/col_len)
		return average
	def get_job(self,job_number,job_num_column_name: str = None):
		"""return rows of given job_number"""
		if job_num_column_name == None:
			job_num_column_name = self.job_num_col_name

		job_rows = self.dataset.loc[self.dataset[job_num_column_name] == job_number]
		return job_rows
	def __get_non_duplicates(self,col_name:str) -> list:
		"""Returns non-duplicate values of a specified column as a list"""
		values = self.dataset[col_name].tolist()
		values = list(set(values)) #trick to remove duplicates
		return values
	def get_job_nums(self,col_name:str=None) -> list:
		"""returns all job numbers found in dataset"""
		if col_name == None:
			col_name = self.job_num_col_name
		values = self.__get_non_duplicates(col_name)
		return values
	def get_job_names(self,col_name:str=None) -> list:
		"""returns all job names found in dataset"""
		if col_name == None:
			col_name = self.job_name_col_name
		values = self.__get_non_duplicates(col_name)
		return values


class pd_multi_column(pd_single_column):
	def __init__(self, dataset: pd.DataFrame,non_zeros: bool = True) -> None:
		"""
		Pandas Extension to take labor averages across multiple columns, but can be used for any use case
		where you need to sum() columns based on conditionals & average across a different column.	
		"""
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
		"""wrapper of superdivide where multiple columns can get divided by the same column to produce data.
		Output: (averages,calculation units)
		"""
		averages = {}
		for col_name in col_1_list:
			averages[col_name] = self.superdivide(col_name,col_2_name)
		units = "Units = Type/Hour"
		return (averages,units)

	def multi_mask(self,non_zero_col: str,zero_columns: Union[list,tuple]):
		"""Takes multiple column names + one column that must be greater than zero & returns mask of all conditions met. IE -> mask.all()"""
		nan = float('nan') # Constant
		eval_str = f"(self.dataset['{non_zero_col}'] > 0)"
		#| self.dataset['{col}'].isna()#USE FOR NAN CASE BUT not needed if you replace NaN with 0's
		for col in zero_columns:
			eval_str += f" & (self.dataset['{col}'] == 0)" # added per iterable
		mask = eval(eval_str)
		# print(f"Mask {non_zero_col} Mask Input:\n{eval_str}\n")
		return mask
	def superdivide_multimask(self,non_zero_col: str,zero_columns: Union[list,tuple],hour_col: str) -> Union[float,int]:
		"""wrapper of multi_mask that uses multi_mask & superdivide to return work/hour for single line item"""
		final_mask = self.multi_mask(non_zero_col,zero_columns)
		filtered_rows = self.dataset[final_mask] #new dataset already masked
		work = self.sum_column(non_zero_col,new_dataset=filtered_rows)
		hours = self.sum_column(hour_col,new_dataset=filtered_rows)
		print(f"For {non_zero_col} Column, Jobs {self.view_jobs(filtered_rows)} were used.")
		work_per_hour = work/hours
		return work_per_hour
	def all_multimask(self,labor_columns: list[str],hours_col:str,units: str = "Items/Hour") -> Tuple[dict,str]:
		"""Calculates Work/Hour for all columns in labor_columns"""
		all_labor_per_hour = {}
		for col in labor_columns: #loop the amount of columns you have
			local_list = deepcopy(labor_columns)
			current_col = local_list.pop(local_list.index(col))
			all_labor_per_hour[col] = self.superdivide_multimask(current_col,local_list,hours_col)
		return (all_labor_per_hour,units)
	def view_jobs(self,dataset: pd.DataFrame = None,job_col: str = None):
		if type(dataset) == type(None):
			# New Dataset Use
			dataset = self.dataset
		if job_col == None:
			job_col = self.job_num_col_name

		all_nums = dataset[job_col]
		job_nums = []
		[job_nums.append(num) for num in all_nums if num not in job_nums]
		return job_nums

class load_csv:
	def __init__(self,csv_path):
		self.csv_path = csv_path
		self.dataset = pd.read_csv(csv_path)

class calculations(load_csv):#job number specific
	def __init__(self,csv_path):
		super().__init__(csv_path)

def test_main():
	data_path = r"S:\Personal Folders\Databases\Cleaned_Dataset_testing.csv"
	job = 4670
	calcs = calculations(data_path)
	calcs.sum(job,"fiber_terminated")

if __name__ == '__main__':
	test_main()