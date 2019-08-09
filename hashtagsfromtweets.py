import tweepy
import csv
import json
import time
import pandas as pd
import re
import itertools

Access_token = <access_token>
Access_token_secret = <access_secret>
API_secret_key = <api_secret>
API_key = <api_key>

auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(Access_token, Access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

Tweet_File = "Tweets.csv"
attribute_file = "Extracted_Attributes1.txt"

data = pd.read_csv(Tweet_File,header =None)

def extract_attributes(tweet):
    attributes = []
    
    for part in tweet.split():
        if part.startswith('@') or part.startswith('#'):
            if part.endswith(':'):
                part = part[:-1]
            attributes.append(part)
    
    return attributes

tweetCount=0
attribute_list =[]

for tweet in data[1]:
    attributes = extract_attributes(tweet)  
    attribute_list.append(attributes)
    
    if tweetCount % 100000 == 0:
        print(tweetCount)
    
    tweetCount = tweetCount + 1
    
attribute_list = list(itertools.chain.from_iterable(attribute_list))

with open(attribute_file, 'w+') as file:
    for item in attribute_list:
        item=' '.join(re.sub("(https:.*)|(x\S*)|[.:,\"]"," ",item).split())
        item = item.replace('\\n','')
        item = item.replace('\\','')
        item = item.replace('\'', '')
        if item.isdigit():
            item = re.sub('[0-9]','', item)
        if len(item)!=1:
            file.write("{}\n".format(item))
file.close()
