# import modules 


import requests
import time 
import numpy as np
from datetime import datetime
import time
import os
import json

# get top 100 coins and save the list of the names
# get past 60 days of data (hourly) and get std of each. 

list_cap = 50 
date_cutoff = 60
std_cutoff = 5
coin_list = []


end_point = 'https://api.coingecko.com/api/v3/coins'
volume_end_point = end_point + '{}/market_chart?vs_currency={}&days={}'.format(coin_id, against, days)
coin_list_end_point = end_point + ('/markets?vs_currency=usd&order=market_cap_desc&per_page={}&page=1&sparkline=false').format(list_cap)

def get_coin_list():
	api_response = requests.get(coin_list_end_point)
	api_data = api_response.json()

	for i in api_data:
		coin_list.append(i['id'])

	return coin_list


get_coin_list()
print (coin_list)

# get past hour of data (minutely) and add them together

# for loop to compare the last hourly data to the std. 
# append to outlier list if it's over STD_CUT times of the std 
# append the name, volume, price, ranking, and how many times of std is over. 

# save result in dict json them save 


