##################################################################################################
# 1) Create Constants
	#a Work Completed Constants including rough-in, (term,test,label), etc
	#b Completion Date
	#c Hours Done
# 2) Manage/Update Constants
##################################################################################################
# 3) Completed Calculator
	#AA single_JSON_counts() --> use self.get_fields() from open_JSON() with a list to get all the required fields and populate a dictionary
	#a Create Counts --> First Pass in __init__():
	#b opened_files_event_handler --> so we don't open already calculated files
	#c Update Counts --> if already created, update counts
		#i Includes files_event_handler_list
		#ii ONLY counts up new files
# 4) Job Calculations
	#a Completed vs Expected Completion
	#b Hours Done vs Expected Hours
##################################################################################################
# 5) Alerting (Email or Slack) --> Slack use requests.post() and webhook() integration
	#a. alert if nothing done on a given day
	#b. alert if behind schedule
	#c. weekly alerts on how much work is done
	#d. daily log NOT turned in...?
# 6) Excel_Output
	#output important data into job specific excel file, could be attached as a link in emails


class daily_reports_pickle():
	def open_pickle(pickle_path):
		all_reports = open(pickle_path,"wb")
	def save_pickle(dict_obj,output_path):
		pck.dump(dict_obj,output_path)