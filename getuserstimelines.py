#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import glob
import ast
import time
import os, sys
from twython import Twython
from tqdm import tqdm

'''
Get as many tweets as possible for each user provided
'''


print('Loading Users...')
df = pd.read_csv('./tables/ncu1k.csv', usecols=['user'])

#get unique userids
users = df['user'].apply(ast.literal_eval)
users = set([user['id'] for user in users])

#initialize twython instance
APP_KEY = os.environ.get('APP_KEY')
APP_SECRET = os.environ.get('APP_SECRET')
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET')

#Start twython instance
twython = Twython(
                  APP_KEY,
                  APP_SECRET,
                  OAUTH_TOKEN,
                  OAUTH_TOKEN_SECRET
                  )

user_tweets = {}

#timeline requests limited to 60/min, how to handle?
#Can ask twitter what the limits are at - It returns json as a dict, navigate to remaining 
twython.get_application_rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining']
#BUT these are rate limited as well - 12/min

print(f'Collecting timelines for {len(users)} users... ')
for user in tqdm(users):
	try:
		#why is it only returning my tweets? i think the error lies with how I supply user
		user_tweets[user] = twython.get_user_timeline(user_id=user)
	except:
		#you *can* check how many you have left, but you have even less of that kind of request
		break

df = pd.DataFrame.from_dict(user_tweets), orient='index')

df.to_csv('./tables/ncu1k_timelines.csv')