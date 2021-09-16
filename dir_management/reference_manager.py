# reference manager class for TakeoffAI

# CURRENT STATE

# AutoCount, Text_Count, & ProjectManagementTools (PMT) NEED rewriting to take advantage of below.
# Fastfield Manager & Database Management will be built with this in mind.
from typing import List,Dict
import os

# active combiner for specific directory classes
class dir_joiner:
	def __init__(self,ref_dir):
		self.ref_dir = ref_dir

	def complete_path_creator(self, ref_dict)->Dict:
		"""returns complete paths of the given ref_dict, created in this class"""
		combined_dict = {}
		for key in ref_dict.keys():
			combined_dict[key] = os.path.join(self.ref_dir,ref_dict[key])
		return combined_dict

class takeoffAI_refs(dir_joiner):
	def __init__(self,ref_dir):
		super().__init__(ref_dir)

		# takeoff feature references
		self.auto_count_refs = self.__auto_count__init__()
		self.text_count_refs = self.__text_count__init__()
		self.PMT_refs = self.__PMT__init__()

		# for testing ONLY
		self.root_check = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI"


	@staticmethod
	def __auto_count__init__() -> Dict:
		"""initialize AutoCount file references. Return Dict()"""
		auto_count_refs = {
			"main_sub":r"AutoCount",
			"projects_root":r"Walker Projects"
		}
		return auto_count_refs
	@staticmethod
	def __text_count__init__() -> Dict:
		"""initialize TextCount references. Return Dict()"""
		text_count_refs = {"main_sub":r"TextCount"}
		return text_count_refs
	@staticmethod
	def __PMT__init__() -> Dict:
		"""initialize Project-Management-Tools paths. Return Dict()"""
		pass

class database_refs(dir_joiner):
	def __init__(self,ref_dir=None):
		super().__init__(ref_dir)
		# Complete References including Dir
		self.complete_database_locations = self.__FTP_refs__init__()
	@staticmethod
	def __FTP_refs__init__()->Dict:
		complete_paths = {
			"FTP_Dir": r"S:\Personal Folders\FTP\Dailys",
			"daily_pdfs_dir": r"S:\Personal Folders\Job Dailys",
			"daily_json_dir": r"S:\Personal Folders\Databases\all_jsons" #NEED TO CREATE
		}
		return complete_paths

if __name__ == '__main__':
	root_path = r"C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI"
	takeoffAI_path_class = takeoffAI_refs(root_path)

	database_ref_cls = database_refs() #root_path optional, because since all paths are hard

	print(f"takeoff ref_dir: {takeoffAI_path_class.ref_dir}")
	print(f"database_ref:{database_ref_cls.ref_dir}")