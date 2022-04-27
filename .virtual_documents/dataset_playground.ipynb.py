import os
import pandas as pd
pd.set_option("display.max_columns", None)


data_path = r"S:\Personal Folders\Databases\Cleaned_Dataset.csv"


data = pd.read_csv(data_path,index_col=0)


info = list(data)
info


os.getcwd()
from FastField_Management.functions.calculation import pd_multi_column
import math


calculator = pd_multi_column(data,non_zeros = True)


calculator.dataset


work_cols = ['copper_terminated','copper_test_label','copper_cables_roughed',
             'fiber_terminated','fiber_test_labeled','fiber_roughed_FT']
daily_hours = "crew_total_daily_hours"
values,_ = calculator.all_multimask(work_cols,daily_hours)


for item in values:
    if values[item] > 0:
        print(f"{item}: {1/values[item]} per/unit")
    else:
        print(f"{item}: {values[item]}")


tmp = data.loc[0:2]
zero = tmp.loc[0,'copper_terminated']
NaN = tmp.loc[2,'copper_terminated']


text_path = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\Walker Projects\5690 Union Sanitation\Misc_Files\Key word search text\AV.txt"


with open(text_path,"r") as f:
    txt = f.read()
text_list = txt.splitlines()
text_list
