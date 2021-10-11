import os
import pandas as pd


data_path = r"S:\Personal Folders\Databases\Cleaned_Dataset.csv"


data = pd.read_csv(data_path,index_col=0)


data.loc[data["JI_job_number"]==5602]
