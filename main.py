import requests
import time 
import numpy as np
from datetime import datetime
import time
import os
import json

list_cap = 100
day_cutoff = 60
# Minutely data will be used for duration within 1 day, 
# Hourly data will be used for duration between 1 day and 90 days, 
# Daily data will be used for duration above 90 days.

std_cutoff = 5
against_currency = "usd"
coin_list = {}
outlier_list = {}


end_point = 'https://api.coingecko.com/api/v3/coins/'
volume_end_point = end_point + '{}/market_chart?vs_currency={}&days={}' # .format inside the later for loop since i is the coin_id
coin_list_end_point = end_point + ('/markets?vs_currency=usd&order=market_cap_desc&per_page={}&page=1&sparkline=false').format(list_cap)

def get_data(url):
	api_response = requests.get(url)
	return api_response.json()

def get_coin_list():

	api_data = get_data(coin_list_end_point)

	api_response = requests.get(coin_list_end_point)
	api_data = api_response.json()

	for i in api_data:
		coin_list[i['id']] = {}
	return coin_list

def get_std(i):

	# i is the coin_id
	api_data = get_data((volume_end_point).format(i, against_currency, day_cutoff))

	# get raw volumes into the list volume_data
	volume_data = []
	for n in api_data['total_volumes']:
		volume_data.append(n[1])

	# the first one is the latest hourly volume, 
	coin_list[i]['volume_std'] = np.std(volume_data[1:])
	coin_list[i]['last_hour_volume'] = volume_data[0]
	coin_list[i]['std_multi'] = round((coin_list[i]['last_hour_volume'] / coin_list[i]['volume_std']), 2)


get_coin_list()

# init 
for i in coin_list:
	get_std(i)
	print (i, coin_list[i])

	# api limit @ 100 per min
	time.sleep(0.7)

# Save outliers to outlier_list
for i in coin_list:
	if coin_list[i]['std_multi'] > std_cutoff:
		outlier_list[i] = coin_list[i]

print (outlier_list)


