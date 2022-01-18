import webbrowser
from typing import List
from googlesearch import search

class text_file_converter:
	def __init__(self,txt_file_path) -> None:
		self.txt_file_path = txt_file_path
		self.text_file = open(self.txt_file_path,'r')

	def to_list(self) -> List[str]:
		"""converts text file to list based on each row in the text file"""
		strings = [line.rstrip() for line in self.text_file]
		return strings


class GoogleSearchManager:
	def __init__(self) -> None:
		pass
	def search_urls(self,terms_list: str) -> None:
		"""google search and open url tab for list of strings to search"""
		for term in terms_list:
			url = f"https://www.google.com.tr/search?q={term}"
			webbrowser.open_new_tab(url)
	def search(self,terms_list: str, num_results: int = 5) -> List[List[str]]:
		"""wrapper of googlesearch.search(). Returns defined number of webpages from google search"""
		results = []
		for term in terms_list:
			results.append(search(term,num_results=num_results))
		return results

def text_main():
	file_path = r"S:\Shared Folders\Steven\Quotes\5600\5674 - GNE B38 AV Budget\Quote and Bid\James Automation Stuff\BOM.txt"
	text_converter = text_file_converter(file_path)
	list_text = text_converter.to_list()
	print(list_text)

def GSM_main():
	search_params = ['Crestron MPC3-102-B', 'Shure UA864US,US864US', 'Bi-Amp BIAMP DP8', 'Logitech Rally', 
	'Shure MXA910-60CM, BIAMP Parle TCM-1 Pendant', 'Crestron GLS-0DT-C-CN', 'Crestron TSS-770-W-S-LB Kit w/ Mount', 
	'Crestron TSS-770-W-S-LB Kit w/ Mount', 'Bi-AMP DP6', 'Middle-Alantic DWR-16-22PD', 'NEP NP-PA1004UL w/ NP417ZL', 
	'DaLITE Professional Electrol 38700', 'PEERLESS DS-VW795-QR w/ACC-V900X', 'LG LG 98UH5F-H', 'Google Jamboard 5J.F3L14.A21', 
	'NEC X551UN', 'Google Jamboard TBD', 'LG 75UH5F-H', 'LG 55UH5F-H + Chief TS525TU', 
	'Aopen Chromebox Aopen Chromebox Commericial 2 Mini PC']

	GSM = GoogleSearchManager()
	GSM.search_urls(search_params) # open searches as google tabs
	# website_results = GSM.search(search_params,num_results=1) # return found websites as urls. returns 5 as default
	# print(website_results)


if __name__ == '__main__':
	GSM_main()
