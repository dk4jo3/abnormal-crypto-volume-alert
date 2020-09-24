import requests
import time 
from datetime import datetime
import numpy as np
import time
import os
import json

list_cap = 100
day_cutoff = 90
# Minutely data will be used for duration within 1 day, 
# Hourly data will be used for duration between 1 day to 90 days, 
# Daily data will be used for duration above 90 days.

std_cutoff = 3
against_currency = "usd"
coin_list = {}
outlier_list = {}
dataDict = {} #main dict for JSON export


end_point = 'https://api.coingecko.com/api/v3/coins/'
volume_end_point = end_point + '{}/market_chart?vs_currency={}&days={}' # .format inside the later for loop since i is the coin_id
coin_list_end_point = end_point + ('/markets?vs_currency=usd&order=market_cap_desc&per_page={}&page=1&sparkline=false').format(list_cap)

def get_data(url):
	api_response = requests.get(url)
	return api_response.json()

def export_JSON(directory, dict_name):
	filename = directory
	with open(filename, 'r') as f:
	    data = json.load(f)

	    # overwrite existing obj in json
	    print (data)
	    data = dict_name

	os.remove(filename)
	with open(filename, 'w') as f:
	    # sort key = False to remain the key order
	    json.dump(data, f, indent=4, sort_keys=False)

def get_coin_list(): #get a list of top 100 coin with their id and symbol.

	api_data = get_data(coin_list_end_point)
	api_response = requests.get(coin_list_end_point)
	api_data = api_response.json()

	for i in api_data:
		coin_list[i['id']] = {}  #i[id] is the coin id 
		coin_list[i['id']]['symbol'] = (i['symbol']).upper() 
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
	coin_list[i]['volume_mean'] = np.mean(volume_data[1:])
	coin_list[i]['last_hour_volume'] = volume_data[0]
	coin_list[i]['upper_std'] = round(((coin_list[i]['last_hour_volume'] - coin_list[i]['volume_mean']) / coin_list[i]['volume_std']), 4)


get_coin_list()

# init 
for i in coin_list:
	get_std(i)
	dataDict[i] = coin_list[i]
	print (i, coin_list[i])

	# api limit @ 100 fetch per minute
	time.sleep(0.7)

print (dataDict)

# save time to dict 
now = datetime.now()
current_time = now.strftime("%b %d %Y %H:%M:%S")
dataDict['time'] = current_time


export_JSON('volumeData.json', dataDict)
