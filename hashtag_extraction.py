import tweepy
import csv
import json
import time

Access_token = <access_token>
Access_token_secret = <access_secret>
API_secret_key = <api_secret>
API_key = <api_key>

auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(Access_token, Access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

woeid_path = <path to woeid file>
hashtag_tag = <path to hashtag file>
workingid = <path to id file>

count = 0

for i in range(100):
    f = open(woeid_path, "r")
    tagfile = open(hashtag_tag, "a")
    woeid_work = open(workingid,"a")
    
    for id in f:
        try:
            trends1 = api.trends_place(int(id))
            data = trends1[0]
            trends = data['trends']
            
            for trend in trends:
                tagfile.write(trend['name'])
                tagfile.write("\n")
            
            woeid_work.write(id)
            print(count)
            count = count + 1
        except tweepy.TweepError as e:
            print(int(id))
            print(e)
            continue
    print(i)
