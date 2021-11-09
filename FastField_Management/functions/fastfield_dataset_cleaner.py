from typing import List, Dict
import pandas as pd

#Open "Raw Dataset" and Scrub it into "Clean Dataset"

#1) One Class for PandaDataframe Controls
#2) Another Class Specific to which Cols to rename, and which to keep, etc

cols_to_keep = ['userName', #'Unnamed: 0', ### add if needed 
	'JI_dailyDate', 'JI_global_foreman_ReportBy', 'JI_global_project_manager', 'JI_job_number', # if needed
	'JI_project_name', 
	'FA_Access_Doors_Pulled', 'FA_Access_fire_alarm_cable_pulled_ft',
	'copper_terminated','copper_test_label' ,'copper_cables_roughed',
	'crew_names', 'crew_total_daily_hours', 'crew_total_members_on_site', 
	'TimeMaterial_Desciption', 'TimeMaterial_Hours', 
	'defect_desciption', 'defect_drawing_ref', 'defect_location', 'defect_spec_num', 
	'delay_calendar_ext', 'delay_company_at_fault', 'delay_man_hours', 'delay_weather_conditions', 
	'delay_weather_notes', 'delay_why',
	'devices_AV_installed', 'devices_CCTV_installed', 'devices_fire_alarm_installed', 'devices_wap_installed',  
	'fiber_terminated','fiber_test_labeled', 'fiber_roughed_FT',
	'foreman_additional_comments', 'foreman_completion_date', 'foreman_signature',
	'idf_cabletray_installed_ft', 'idf_cop_patch_panels_term', 'idf_fiber_panels_termed', 'idf_racks_installed',  
	'walker_inline_cover_walkerInfo', 'work_materials_on_site', 'work_other'] #cols to keep
# HELPER FUNCTIONS TO CREATE DICTIONARY OF ABOVE, AND CHANGE ONLY THE ONES YOU WANT TO RENAME
cols_name_map = dict(zip(cols_to_keep,cols_to_keep))
###DROP NAME CHANGES HERE###
cols_name_map['JI_job_number'] = "Job Number"
cols_name_map['JI_dailyDate'] = "Daily Date"
cols_name_map['JI_global_foreman_ReportBy'] = 'Report By (Foreman)'
cols_name_map['TimeMaterial_Desciption'] = 'T&M Description'
cols_name_map['TimeMaterial_Hours'] = 'T&M Hours'
cols_name_map['userName'] = 'Account'

##############################################################################################################################
###########################HELPER FUNCTIONS FOR CLEANING TEXT IN COLUMNS######################################################
def column_single_list_unpacker(pd_dataset,column_name_tuple=('JI_global_foreman_ReportBy','JI_global_project_manager')):
	for row,cols_info in pd_dataset.iterrows():#dataset rows
		for col in column_name_tuple:# columns to unpack
			str_data = cols_info[col]
			cleaned_str = str_data.strip("]['") #Add .split(', ') for list solution instead, but this is quicker
			pd_dataset.at[row, col] = cleaned_str
	return pd_dataset

def column_helper(pd_dataset,column_name_tuple=('JI_global_foreman_ReportBy','JI_global_project_manager')):
	pd_dataset = column_single_list_unpacker(pd_dataset,column_name_tuple=column_name_tuple)
	return pd_dataset
##############################################################################################################################

def main(raw_dataset_path = r"S:\Personal Folders\Databases\Raw_Dataset.csv", #.csv format
	cleaned_data_path = r"S:\Personal Folders\Databases\Cleaned_Dataset"): #.csv & excel format):
	data = pd.read_csv(raw_dataset_path)

	# UPDATE DATATYPES FOR VIEWING PURPOSES (["name"] becomes "name", etc.)
	data = column_helper(data)

	# UPDATE COLUMN NAMES
	clean_data = data.filter(cols_to_keep)
	clean_data = clean_data.rename(columns=cols_name_map)#,inplace=True) #use list to create order
	# print(clean_data.head())
	# print(clean_data.columns)

	# Save Cleaned Dataset
	clean_data.to_csv("".join([cleaned_data_path,".csv"]))
	clean_data.to_excel("".join([cleaned_data_path,".xlsx"]))

if __name__ == '__main__':
	main()