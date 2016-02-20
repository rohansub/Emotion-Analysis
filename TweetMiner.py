from __future__ import print_function
import json

from TwitterAPI import TwitterAPI
from TwitterKeys import CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET


def mineTweets(username):
    tweet_list = []
    api = TwitterAPI(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)
    r = api.request('statuses/user_timeline', {'screen_name': username})
    for item in r:
        tweet_list.append((item['text'],item['created_at']))
    return tweet_list
