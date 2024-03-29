#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 21:42:51 2020
@author: rob
"""
#import json  datetime
import pandas as pd
import os, sys
import json
from threading import Thread
from twython import TwythonStreamer


assert len(sys.argv) == 2, 'Usage: run pulltweets.py *Your Search Term*'

class globalVars():
  pass

topic = sys.argv[1]

#holds the state of the additional thread
G = globalVars()
G.kill = False

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if data.get('lang') == 'en':
            tweets.append(data)
            print(f'received tweet #{len(tweets)}')
            
        if G.kill:
          print('Tweet collection stopped')
          self.disconnect()
                
    def on_error(self, status_code, data):
        print(status_code,data)
        
        #Stop trying to get data
        self.disconnect()

topic = sys.argv[1]

#initialize twython instance
APP_KEY = os.environ.get('APP_KEY')
APP_SECRET = os.environ.get('APP_SECRET')
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET')

tweets = []
filepath = f'./tables/policy.json'


#Start streamer instance
stream = MyStreamer(
                  APP_KEY,
                  APP_SECRET,
                  OAUTH_TOKEN,
                  OAUTH_TOKEN_SECRET
                  )

def pull_tweets():
  if G.kill == False:
        stream.statuses.filter(track=[topic])
  return

tweetpuller = Thread(target=pull_tweets)
tweetpuller.start()

help = 'h | help : get help\nq | quit : quit and save csv\nc | cancel : quit without saving\n'



def get_cmd(): 
  cmd = input()
  if cmd == 'h' or cmd == 'help':
    print(help)
    return 1
  elif cmd == 'q' or cmd == 'quit':
    G.kill = True
    print('Quitting')
    return 0
  elif cmd == 'c' or cmd == 'cancel':
    G.kill = True
    print('Exiting...')
    sys.exit()
  else:
    print(f'{cmd} not accepted\n{help}')

print(f'Collecting tweets about {topic}!\n{help}')

while get_cmd():
  pass
    
print(f'Saving to {filepath}!')
with open(filepath, 'w') as json_file:
  json.dump(tweets, json_file, allow_nan=False, indent=4)