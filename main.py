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

against_currency = "usd"
coin_list = {}
outlier_list = {}
dataDict = {} #main dict for JSON export


end_point = 'https://api.coingecko.com/api/v3/coins/'
volume_end_point = end_point + '{}/market_chart?vs_currency={}&days={}' # .format inside later for loop since i is the coin_id
coin_list_end_point = end_point + ('/markets?vs_currency=usd&order=market_cap_desc&per_page={}&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d').format(list_cap)

def get_data(url):
	api_response = requests.get(url)

	try: 
		api_response.raise_for_status() 
	except requests.exceptions.HTTPError as e: # Whoops it wasn't a 200 
		return "Error: " + str(e)

	return api_response.json()

def export_JSON(directory, dict_name):
	os.remove(directory)
	with open(directory, 'w') as f:

	    # sort key = False to remain the key order
	    json.dump(dict_name, f, indent=4, sort_keys=False)

def get_coin_list(): #get a list of top 100 coin with their id and symbol.

	api_data = get_data(coin_list_end_point)
	api_response = requests.get(coin_list_end_point)
	api_data = api_response.json()


	for i in api_data:
		coin_list[i['id']] = {}  #i[id] is the coin id 
		coin_list[i['id']]['symbol'] = (i['symbol']).upper() 

		# Save the price data
		coin_list[i['id']]['hour'] = i['price_change_percentage_1h_in_currency']
		coin_list[i['id']]['day'] = i['price_change_percentage_24h_in_currency']
		coin_list[i['id']]['week'] = i['price_change_percentage_7d_in_currency']

		time_list = ['hour', 'day', 'week']
		for n in time_list: 
			if coin_list[i['id']][n] is not None:
				coin_list[i['id']][n] = round((coin_list[i['id']][n]), 2)
			else:
				coin_list[i['id']][n] = 'NA'

	print (coin_list)
	return coin_list

def get_std(i):

	# i is the coin_id
	api_data = get_data((volume_end_point).format(i, against_currency, day_cutoff))

	# get raw volumes into the list volume_data
	volume_data = []

	try: 
		for n in api_data['total_volumes']:
			volume_data.append(n[1]) #n[0] is the time code

		# the last one is the latest hourly volume, 
		coin_list[i]['volume_std'] = np.std(volume_data[:-1])
		coin_list[i]['volume_mean'] = np.mean(volume_data[:-1])
		coin_list[i]['last_24hour_volume'] = volume_data[-1]

		upper_std = round(((coin_list[i]['last_24hour_volume'] - coin_list[i]['volume_mean']) / coin_list[i]['volume_std']), 2)

		if np.isnan(upper_std) == False:
			coin_list[i]['upper_std'] = upper_std
		else: 
			coin_list[i]['upper_std'] = 0
	except Exception as e: 
		print (e)

	# coin_list[i]['upper_std'] = round(((coin_list[i]['last_24hour_volume'] - coin_list[i]['volume_mean']) / coin_list[i]['volume_std']), 2)


get_coin_list()

# init 
for i in coin_list:
	get_std(i)

	#check is std or mean is NaN, 
	if np.isnan(coin_list[i]['volume_std']) or np.isnan(coin_list[i]['volume_mean']) == False:

		# don't edit dict while looping so add to a new dict
		dataDict[i] = coin_list[i]
		print (i, coin_list[i])
	else: 
		pass

	# api limit @ 100 fetch per minute
	time.sleep(1.0)

# save time to dict 
now = datetime.now()
current_time = now.strftime("%b %d %Y %H:%M:%S")
dataDict['time'] = current_time


export_JSON('volumeData.json', dataDict)
