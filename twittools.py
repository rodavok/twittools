#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 20:03:18 2020

@author: rob
"""

import pandas as pd
import os
import time
from tqdm import tqdm
from typing import Generator
from twython import Twython

def start_twython(x='core'):
    #Collect keys
    APP_KEY = os.environ.get('APP_KEY')
    APP_SECRET = os.environ.get('APP_SECRET')
    OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
    OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET')
    if x == 'core':
        #Return twython core api instance
        return Twython(
                      APP_KEY,
                      APP_SECRET,
                      OAUTH_TOKEN,
                      OAUTH_TOKEN_SECRET
                      )
    elif x == 'stream':
        return TwythonStreamer(
                      APP_KEY,
                      APP_SECRET,
                      OAUTH_TOKEN,
                      OAUTH_TOKEN_SECRET
                      )
    else:
        print('Usage:\nstart_twython('core') - Return core api\nstart_twython('stream') - Return streamer api')

def chonker(seq:list, size:int) -> Generator:
    """
    returns a generator which will produce seq in sections of size 
    """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def hydrate_users(id_list:list, twitter:Twython) -> pd.DataFrame:
    '''


    Parameters
    ----------
    users_list : list
        List of ints representing Twitter user ids to hydrate
    twitter : Twython instance
        Authenticated Twython instance
        
        
    Returns
    -------
    hydrated_users_df : pd.DataFrame
        hydrated user information


    '''    
    users = []
    #request in groups of 100 to avoid limits
    for chonk in chonker(id_list, 100):
        for user in twitter.lookup_user(user_id = chonk):
            users.append(user)
    return pd.DataFrame(users)
 
def hydrate_statuses(id_list:list, twitter:Twython) -> pd.DataFrame:
    """


    Parameters
    ----------
    id_list : list
        List of ints representing Twitter status ids to hydrate
    twitter : Twython instance
        Authenticated Twython instance
        
        
    Returns
    -------
    hydrated_users_df : pd.DataFrame
        hydrated user information


    """
    statuses = []
    #request in groups of 100 to avoid limits
    for chonk in chonker(id_list, 100):
        for tweet in twitter.lookup_status(status_id = chonk):
            statuses.append(tweet)
    return pd.DataFrame(statuses)

def rate_limit_request(twython, resource, endpoint, parameters, window):
    """
    run API requests without exceeding rate limits


    Parameters
    ----------
    twython : API instance
    resource : API resource category (i.e. 'statuses')
    endpoint : API endpoint (need the direct twitter API for rate limit status, and the twython method that uses it)
    parameter_list : options to pass to request
    window : length of the window, may be able to get this from ratelimitstatus()['resources'][resource]

    Returns
    -------
    results : dictionary of parameter_list and its request results


    """
    results = {}

    #check number of remaining requests 
    starting_requests = requests_remaining = int(twython.get_application_rate_limit_status()['resources'][resource][endpoint]['remaining'])

    print(f'{requests_remaining} requests remaining')

    for element in tqdm(parameter_list):
        if requests_remaining > 0:
            try:
                results[element] = twython.#endpoint?(element)
            except:
                pass
            if requests_remaining >= starting_requests:
                #start timer if this was the first request
                end_time = time.time() + window*60 + 10
            requests_remaining -= 1
        else:
            #wait until window rolls over
            while time.time() < end_time:
                time.sleep(15)
            starting_requests = requests_remaining = int(twython.get_application_rate_limit_status()['resources'][resource][endpoint]['remaining'])

    return results

