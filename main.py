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


current_time = int(time.time())
print (current_time)

# get past hour of data (minutely) and add them together. them append to dict 

# for loop to compare the last hourly data to std. 
# append to outlier list if it's over STD_CUT times of the std 
# append the name, volume, price, ranking, and how many times of std is  over. 


end_point = 'https://api.coingecko.com/api/v3/'
