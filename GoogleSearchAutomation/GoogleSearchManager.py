import webbrowser
from typing import List,Type, Optional,Tuple
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import statistics
import pandas as pd

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
	def search_urls(self,terms_list: List[str]) -> None:
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
		self.prices = None #allows type hints to work

		self.CSS_selectors = [".HRLxBb, .rgHvZc",".HRLxBb",".rgHvZc"] #Google Shop Selectors
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
			time.sleep(.05) #Google Will Return Failed Page if you Request to many times in a second
	def __convert_to_soup(self):
		self.soup_pages = [BeautifulSoup(result.content,"html.parser") for result in self.final_res]
	def __filter_soup(self) -> None:
		"""filters soup results from requests"""
		self.all_items = [soup.select(self.CSS_selectors[0]) for soup in self.soup_pages]
		self.name_items = [soup.select(self.CSS_selectors[2]) for soup in self.soup_pages]
		self.price_items = [soup.select(self.CSS_selectors[1]) for soup in self.soup_pages]
	def __extract_soup(self) -> None:
		"""Takes filter_soup and creates (product,price) pairs in a list"""
		def grab_item_names(list_of_CSS: List[str]) -> List[str]:
			"""Helper to Extract Item Names from soup"""
			def combine_strings(str_list: List[str]) -> str:
				"""takes CSS literals and combine text together."""
				final_str = "".join([string.get_text() for string in str_list])
				return final_str
			item_names = [combine_strings(list_of_CSS[i].select('a, b')) for i in range(len(list_of_CSS))]
			return item_names
		def grab_item_prices(list_of_CSS: List[str]) -> List[float]:
			"""Helper to Extract Item prices from soup"""
			def string_to_float(string: str):
				clean_string = "".join(i for i in string if i.isdigit() or (i in "-."))
				number = float(clean_string)
				return number
			item_prices = [string_to_float(i.get_text()) for i in list_of_CSS]
			return item_prices
		def list_of_tuples(name_list: List[str],price_list: List[float]):
			"""Pairs Names and Prices as tuple pairs in a list (self.item_pairs)
			& creates a numpy array as strings (self.price_array)"""
			def sort_tuples(tup):
				"""Helper function to sort items based on prices. Descending Order"""
				tup.sort(key = lambda x: x[1],reverse=True)
				return tup

			item_pairs = []
			for item_search in zip(name_list,price_list):
				item_pairs.append(item_search)
			price_array = np.array(sort_tuples(item_pairs))
			return item_pairs,price_array
		self.prices = []
		for names, prices in zip(self.name_items,self.price_items):
			item_names = grab_item_names(names)
			item_prices = grab_item_prices(prices)
			item_pairs, price_array = list_of_tuples(item_names,item_prices)
			self.prices.append((item_pairs,price_array))

	def extract_prices(self):
		"""Extracts [(name,price)] for each google seach passed to the class"""
		self.__requests()
		self.__convert_to_soup()
		self.__filter_soup()
		# [print(f"{names}\n{prices}\n\n") for names,prices in zip(self.name_items,self.price_items)]
		self.__extract_soup()

class GoogleShopDataProcessing:
	def __init__(self,items: Tuple[List[Tuple[str,float]],np.ndarray]):
		"""items: needs to be GoogleShopScraper.prices """
		self.item_datasets = items
		self.float_type = np.float16
		self.excel_file_name = "GoogleSDP_response.xlsx"
	def __convert_to_float_list(self,array: np.array,col: int = 1) -> List[float]:
		"""Helper function to convert string numbers in nd.ndarrays to floating point lists for mathmatical operations"""
		self.data_list = array[:,col].astype(self.float_type).tolist()
		return self.data_list
	def get_max(self,shop_list: np.ndarray) -> Tuple[str,float]:
		"""return max cost of item"""
		name = shop_list[0,0]
		price = shop_list[0,1].astype(self.float_type)
		return (name,price)
	def get_average(self,shop_list: np.ndarray,length: Optional = None) -> Tuple[str,float]:
		if length == None:
			length = len(shop_list[:,0])
		name = shop_list[0,0]
		numbers = shop_list[0:length,1].astype(self.float_type).tolist()
		avg = statistics.mean(numbers)
		return (name,avg)
	def get_variance(self,shop_list: np.ndarray,length: Optional = None) -> Tuple[str,float]:
		if length == None:
			length = len(shop_list[:,0])

		prices = self.__convert_to_float_list(shop_list[0:length,:])
		name = shop_list[0,0]
		variance = statistics.variance(prices)
		return (name,variance)
	def all_averages(self,num_rows: Optional[int] = None) -> List[Tuple[str,float]]:
		"""Wrapper of get_average() for self.item_datasets"""
		all_avgs = [self.get_average(array,num_rows) for _,array in self.item_datasets]
		return all_avgs
	def all_variance(self,num_rows: Optional[int] = None) -> List[Tuple[str,float]]:
		"""Wrapper of get_variance() for self.item_datasets"""
		all_vars = [self.get_variance(array,num_rows) for _,array in self.item_datasets]
		return all_vars
	def all_max(self) -> List[Tuple[str,float]]:
		"""Wrapper of get_max() for self.item_datasets"""
		all_maxs = [self.get_max(array) for _,array in self.item_datasets]
		return all_maxs
	def __tuples_to_npArray(self,dataset: List[Tuple[str,float]]) -> np.ndarray:
		"""Helper Function that convert List of Tules to np.ndarray"""
		return np.asarray(dataset)
	def __combine_Arrays(self,avgs,variances,maxs) -> pd.DataFrame:
		"""Helper Function that combines shopping information into one dataset for readability"""
		final_dataset = np.column_stack((avgs[:,0],avgs[:,1],maxs[:,1],variances[:,1]))
		data = pd.DataFrame(final_dataset)
		data.columns =['Part Number', 'Average Price', 'Max', 'Variance']
		data[["Average Price","Max","Variance"]] = data[["Average Price","Max","Variance"]].apply(pd.to_numeric)
		return data
	def get_all(self,num_rows: Optional[int] = None, save_excel: bool = False) -> pd.DataFrame:
		"""gets all statistical properties for list of price objects"""
		avgs = self.__tuples_to_npArray(self.all_averages(num_rows))
		variances = self.__tuples_to_npArray(self.all_variance(num_rows))
		maxs = self.__tuples_to_npArray(self.all_max())
		data = self.__combine_Arrays(avgs,variances,maxs)
		
		if save_excel:
			data.to_excel(self.excel_file_name)
			print("Excel File Save Succesful")
		return data

class GoogleShopMain:
	def __init__(self,search_params) -> None:
		"""Wrapper Class for GoogleShopDataProcessing & GoogleShopScraper Classes"""
		self.search_params = search_params
	def run(self,num_of_items: int = 5, excel_save: bool = False) -> pd.DataFrame:
		"""Takes self.search_params and runs both classes, and returns pd.DataFrame & saves if set to true"""
		GSS = GoogleShopScraper(self.search_params)
		GSS.extract_prices()

		GSDP = GoogleShopDataProcessing(GSS.prices)
		data = GSDP.get_all(num_rows=num_of_items,save_excel=excel_save)
		return data

def shop_main():
	search_params = ['Crestron MPC3-102-B','crestron dm-tx-200-c-2g-w-t',"toothpaste"]
	# ["toothpaste, super mario sunshine, winny the poo"]
	GSM = GoogleShopMain(search_params)
	data = GSM.run(num_of_items=5,excel_save=True)
	print(data)

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
	#5) Check and make sure google isn't changing the CSS Keys. Seems scrambed, but does the scramble change?
	#6) Change Class for Single Use...? --> Or make it iteratable for varying sizes?
