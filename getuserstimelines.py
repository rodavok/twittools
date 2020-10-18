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

def start_twython():
	#Collect keys
	APP_KEY = os.environ.get('APP_KEY')
	APP_SECRET = os.environ.get('APP_SECRET')
	OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
	OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET')
  #Return twython instance
	return Twython(
                  APP_KEY,
                  APP_SECRET,
                  OAUTH_TOKEN,
                  OAUTH_TOKEN_SECRET
                  )

#create twython object
twython = start_twython()

print('Loading Users...')
df = pd.read_csv('./tables/ncu1k.csv', usecols=['user'])

#get unique userids
users = df['user'].apply(ast.literal_eval)
users = set([user['id'] for user in users])

#check number of remaining requests 
starting_requests = requests_remaining = int(twython.get_application_rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining'])

print(f'{requests_remaining} requests remaining')

users_tweets = {}

print(f'Collecting timelines for {len(users)} users... ')

for user in tqdm(users):
	user_tweets = []
	timeline_chunk = ['init']
	max_id = 0

	while len(timeline_chunk) > 0:
		if requests_remaining > 0:
			try:
				if max_id == 0:
					#can't use inf as max ID because it's a float, can't use an arbitrarily large number, this is dumb
					timeline_chunk = twython.get_user_timeline(user_id=user, count=200, trim_user=1, include_rts=1)
				else:
					timeline_chunk = twython.get_user_timeline(user_id=user, count=200, trim_user=1, max_id=max_id, include_rts=1)

			#If a users profile is protected, it will return an error, ignore and move to next user
			except:
				timeline_chunk = []

			if requests_remaining >= starting_requests:
				#start timer if this was the first request
				end_time = time.time() + 15*60 + 10
			requests_remaining -= 1

		else:
			#check if window has rolled over every 15 sec
			while time.time() < end_time:
				time.sleep(15)
			#reset request count
			starting_requests = requests_remaining = int(twython.get_application_rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining'])

		if len(timeline_chunk) > 0:
			user_tweets += timeline_chunk
			max_id = min([i['id'] for i in timeline_chunk])-1

	if len(user_tweets) > 0:
		users_tweets[user] = user_tweets

df = pd.DataFrame.from_dict(users_tweets, orient='index')

df.to_csv('./tables/ncu1k_timelines.csv')
