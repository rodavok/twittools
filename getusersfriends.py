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
df = pd.read_csv('./tables/ncu1k.csv')

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

hydrated_users = {}

#requests limited to 15/15mins
with Bar(f'Collecting Friends for {len(users)} users... ', max=len(users), suffix='%(eta)d%%') as bar:
	for user in users:
		hydrated_users[user] = twython.get_friends_ids(params={user})
		time.sleep(61)
		bar.next()

df = pd.DataFrame.from_dict(hydrated_users)

df.to_csv('./tables/tweetersfriends.csv')