import webbrowser
from typing import List
from googlesearch import search
from bs4 import BeautifulSoup
import requests

#new imports for trying to get dynamic loaded html
import json
import urllib

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

class GoogleShopScraper(GoogleSearchManager):
	def __init__(self,terms_list) -> None:
		"""Primary class to search a Google Shopping Landing Page Url and Return a designated number of costs and titles."""
		self.terms_list = terms_list
		self.__create_urls()

		self.CSS_selectors = ".HRLxBb, .rgHvZc" #selector for pricing...? --> Make sure google does NOT scramble
	def __create_urls(self) -> None:
		"""appends search terms into google shop url for webscraping"""
		url = lambda term: f"https://www.google.com.tr/search?q={term}&tbm=shop"
		self.urls = [url(term.replace(" ","%20")) for term in self.terms_list]
	def __requests(self):
		"""Returns Requests from Google Shop url searches"""
		self.final_res = []
		for url in self.urls:
			res = requests.get(url)
			res.encoding = "utf-8"
			self.final_res.append(res)
			assert res.status_code == 200
	def __convert_to_soup(self):
		self.soup_pages = [BeautifulSoup(result.content,"html.parser") for result in self.final_res]
	def __filter_soup(self):
		"""filters soup results from requests"""
		self.items = [soup.select(self.CSS_selectors) for soup in self.soup_pages]
	def extract_prices(self):
		self.__requests()
		self.__convert_to_soup()
		self.__filter_soup()
		# print(self.soup_pages[0])
		print(self.items[0])
		print(f"\n\n\n{self.items[1]}")



def shop_main():
	search_params = ['Crestron MPC3-102-B','crestron dm-tx-200-c-2g-w-t']
	GSS = GoogleShopScraper(search_params)
	GSS.extract_prices()

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
	shop_main()
	# To do List #
	#1) Convert Notebook Code into Class Functions for sorting information
	#2) Save in excel format with orginial google searches for ease of copy-paste
	#-------------------------------------------------------------------------------------
	#3) Write function to take highest 3 google prices & make them a column each for use.
	#4) Make averaging of top 3-5 prices and use that one for final
	#-------------------------------------------------------------------------------------
	#5) Check and make sure google isn't changing the CSS Keys. Seems scrambed, but does the scramble change?
	#6) Change Class for Single Use...? --> Or make it iteratable for varying sizes?
