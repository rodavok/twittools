#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import ast
import time
import os
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

#check number of remaining requests 
starting_requests = requests_remaining = int(twython.get_application_rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining'])

print(f'{requests_remaining} requests remaining')

print(f'Collecting timelines for {len(users)} users... ')

for user in tqdm(users):
	if requests_remaining > 0:
		try:
			user_tweets[user] = twython.get_user_timeline(user_id=user)
		except:
			pass
		if requests_remaining >= starting_requests:
			#start timer if this was the first request
			end_time = time.time() + 15*60 + 10
		requests_remaining -= 1
	else:
		#wait until window rolls over
		while time.time() < end_time:
			time.sleep(15)
		starting_requests = requests_remaining = int(twython.get_application_rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining'])

df = pd.DataFrame.from_dict(user_tweets, orient='index')

df.to_csv('./tables/ncu1k_timelines.csv')