#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import glob
import ast
import time
import os, sys
from twython import Twython
from progress.bar import Bar

'''
get a list of unique users given a csv of tweets
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

friends_users = {}

#requests limited to 15/15mins
with Bar(f'Collecting Friends for {len(users)} users... ', max=len(users), suffix='%(eta)d%%') as bar:
	for user in users:
		friends_users[user] = twython.get_friends_ids(params={user})
		time.sleep(61)
		bar.next()


#keys are used as column names by default, I probably want to switch but the cursor stuff is confusing me 
#IF i want to use the keys as rows, use option orient='index')
df = pd.DataFrame.from_dict(friends_users)

df.to_csv('./tables/tweetersfriends.csv')