#Event_Handler Code --> Originally intended to keep track of which json's had already been added to dataset
import os
import pickle as pck
from typing import List

class event_handler:
	def __init__ (self,events = []):
		self.events = list(events)
	
	def new_event_check(self, new_event):
		"""takes in event name and adds it to events log if it doesn't exist"""
		if new_event in self.events:
			return None
		self.events.append(new_event)
		return True
	def add_events(self, new_events: List, save_path=None):
		"""Loops through list and saves new handler lists in pickle if save_path != None"""
		new_handler = self.events + new_events #append lists together
		new_handler = list(set(new_handler)) #remove copies
		self.events = new_handler #update handler for saving
		if save_path != None:
			self.pickle_save(save_path)
			print(f"Save Complete @:\n{save_path}")

	def pickle_save(self,pickle_path,file_name="event_list.pkl"):
		if not pickle_path.endswith(".pkl"):
			complete_path = os.path.join(pickle_path,file_name)
		else:
			complete_path = pickle_path
		with open(complete_path,'wb') as f:
			pck.dump(self.events,f)
			f.close()

class events_loader(event_handler):
	def __init__(self,input_dir,pickle_complete_file):
		#variables
		self.input_dir = input_dir
		self.pickle_complete_file = pickle_complete_file
		#all events via file type in folder
		self.initial_events = self.grab_files(input_dir,file_type=".json")
		#Return 'new_events' ONLY
		super().__init__(self.__open_event_handler(pickle_complete_file))
		self.new_files = [f for f in self.initial_events if f not in self.events] #grab files not in events

	def close(self):
		"""can be called to update handler.pck after using self.new_files for given purpose"""
		self.add_events(self.new_files,save_path=self.pickle_complete_file)

	@staticmethod
	def __open_event_handler(event_pkl_path):
		"""
		Helper Function to Open an Already existing event handler and return instant of event_handler
		"""
		try:
			with open(event_pkl_path,'rb') as f:
				loaded_list = pck.load(f)
			# print(loaded_list)
			return loaded_list
		except:
			print("Event Handler Does Not Exist. Please make sure your event_pkl_path is correct.\
				If this is your first run of the event_handler, please run 'initialize_handler'.")
			print("returning empty event_handler")
			return []
	@staticmethod
	def grab_files(input_dir,file_type=".json"):
		"""Grab all files of a specified type for handler"""
		json_files = [f for f in os.listdir(input_dir) if f.endswith(file_type)]
		return json_files
	def grab_new_events(self):
		"""wrapper to return new events found at __init__"""
		return self.new_files
	def view_handler(self):
		"""view existing events table"""
		print(self.events)

def event_main(input_dir = r"S:\Personal Folders\FTP\Dailys",database_dir = r"S:\Personal Folders\Databases",
	daily_events_file = r"daily_list.pkl"):
	handler = events_loader(input_dir,os.path.join(database_dir,daily_events_file))
	new_events = handler.grab_new_events()
	handler.close() #updates handler & saves
	return new_events

if __name__ == '__main__':
	event_main()