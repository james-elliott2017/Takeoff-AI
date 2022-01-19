from GoogleSearchManager import GoogleShopScraper
import numpy as np
from typing import List


search_params = ['Crestron MPC3-102-B','crestron dm-tx-200-c-2g-w-t']
GSS = GoogleShopScraper(search_params)
GSS.extract_prices()


information = GSS.items[1]
information


def list_to_line(b_list: List):
    final_str = "".join([string.get_text() for string in b_list])
    return final_str

search_strings = [list_to_line(information[i].select('b')) for i in range(len(information)) if iget_ipython().run_line_magic("2", " == 0]")
search_strings


def string_to_float(string: str):
    clean_string = string.replace("$","").replace(",","")
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
