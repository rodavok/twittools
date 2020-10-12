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
get a list of unique users given a csv of tweets
TODO: 
get rate limits directly from twitter
take topic as an argument instead of hardcoding, & save as topic-specific-file with timestamp so as to avoid overwriting (ever)
'''

print('Loading Tweets...')
df = pd.read_csv('./tables/ncu1k.csv', usecols=['user'])

#get unique userids
print('Collecting Users...')
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

user_friends = {}

#requests limited to 15/15mins
print(f'Collecting Friends for {len(users)} users... ')
for user in tqdm(users):
	user_friends[user] = twython.get_friends_ids(params={user})
	time.sleep(61)

df = pd.DataFrame.from_dict(users_friends, orient='index')

df.to_csv('./tables/ncu1kfriends.csv')