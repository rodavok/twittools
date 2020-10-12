#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import glob
import ast
#import time
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

#requests limited to 60/min, how to handle?
#Can ask twitter what the limits are at
twython.get_application_rate_limit_status(params={'statuses/user_timeline'})

print(f'Collecting timelines for {len(users)} users... ')
for user in tqdm(users):
	print(twython.get_application_rate_limit_status(params={'statuses/user_timeline'}))
	user_tweets[user] = twython.get_user_timeline(params={user})

df = pd.DataFrame.from_dict(user_tweets, orient='index')

df.to_csv('./tables/ncu1k_timelines.csv')