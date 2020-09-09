import requests
import time 
import numpy as np
from datetime import datetime
import time
import os
import json

# get top 100 coins and save the list of the names
# get past 60 days of data (hourly) and get std of each. 

list_cap = 5
date_cutoff = 5
# Minutely data will be used for duration within 1 day, 
# Hourly data will be used for duration between 1 day and 90 days, 
# Daily data will be used for duration above 90 days.

std_cutoff = 5
against_currency = "usd"
coin_list = {}


end_point = 'https://api.coingecko.com/api/v3/coins/'
volume_end_point = end_point + '{}/market_chart?vs_currency={}&{}={}'
coin_list_end_point = end_point + ('/markets?vs_currency=usd&order=market_cap_desc&per_page={}&page=1&sparkline=false').format(list_cap)

def get_coin_list():
	api_response = requests.get(coin_list_end_point)
	api_data = api_response.json()

	for i in api_data:
		coin_list[i['id']] = {}
	return coin_list

def get_std(i):
	api_response = requests.get((volume_end_point).format(i, against_currency, 'days', date_cutoff))
	api_data = api_response.json()

	# get raw volumes into a list volume_data
	volume_data = []
	for n in api_data['total_volumes']:
		volume_data.append(n[1])

	# calculate std and put them in the main dict
	coin_list[i]['volume_std'] = np.std(volume_data)


get_coin_list()

for i in coin_list:
	get_std(i)

print (coin_list)



