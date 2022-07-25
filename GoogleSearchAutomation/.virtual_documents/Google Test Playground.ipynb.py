from GoogleSearchManager import GoogleShopScraper,GoogleShopMain,GoogleSearchManager
import numpy as np
from typing import List, Tuple, Iterator,Optional
import time
import statistics
import pandas as pd


# Open Text File (each row is a item in list)
text_file = r"C:\Users\james\Downloads\5669 Building E DAS Material List.txt"
with open(text_file, 'r') as txtFile:
    data=txtFile.read()
    list_of_items = [line.strip() for line in data.split('\n')] #creates list of rows from text file


search_only = GoogleSearchManager()
search_only.search_urls(list_of_items)


search_parameters = ["toothpaste", "super mario sunshine", "winny the poo"]

save_to_excel = True
num_of_datapoints_for_averaging = 5 #takes "#" of most expensive items for averaging and variance


GSM = GoogleShopMain(search_params=search_parameters)
GSM.run(num_of_items=num_of_datapoints_for_averaging,excel_save=save_to_excel)





search_params = ['Crestron MPC3-102-B','crestron dm-tx-200-c-2g-w-t','coolgate toothpaste']
GSS = GoogleShopScraper(search_params)

start = time.time()
GSS.extract_prices()
stop = time.time()
print(f"Processing time for {len(search_params)} items was {stop - start}")


# Check Raw URLs
GSS.urls


#Check Raw Returned Request
GSS.soup_pages[1]





information = GSS.items[0]
information[0].select('a, b')[0].get_text()


def list_to_line(b_list: List[str]) -> str:
    final_str = "".join([string.get_text() for string in b_list])
    return final_str

search_strings = [list_to_line(information[i].select('a, b')) for i in range(len(information)) if iget_ipython().run_line_magic("2", " == 0]")
search_strings


def string_to_float(string: str):
    clean_string = "".join(i for i in string if i.isdigit() or (i in "-."))
    number = float(clean_string)
    return number
search_prices = [string_to_float(information[i].get_text()) for i in range(len(information)) if i%2 get_ipython().getoutput("= 0]")
search_prices


def sort_tuples(tup):
    tup.sort(key = lambda x: x[1],reverse=True)
    return tup


final_data = []
for item_search in zip(search_strings,search_prices):
    final_data.append(item_search)
print(final_data)
final = np.array(sort_tuples(final_data))
print(final)


_,test_array = GSS.prices[0]
num_list = test_array[:,1].astype(np.float16).tolist()
num_list


#Class Already Exists in GoogleSearchManager.py --> Please Use V2 Code for daily use
class GoogleShopDataProcessing:
    def __init__(self,items: Iterator[np.ndarray]):
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


GSDP = GoogleShopDataProcessing(GSS.prices)


data = GSDP.get_all(num_rows=5,save_excel=True)
data


_,array = GSDP.item_datasets[0]
GSDP.get_average(array,length = 5)


GSDP.get_max(array)


GSDP.get_variance(array,length=8)


avgs


varrs


maxs


maxs.shape


data


data[["Average Price","Max","Variance"]] = data[["Average Price","Max","Variance"]].apply(pd.to_numeric)
data


writer = pd.ExcelWriter('fancy.xlsx', engine='xlsxwriter')
df.to_excel(writer, index=False, sheet_name='report')
