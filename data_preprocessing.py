import tweepy
import csv
import pandas as pd
import math
from tweepy import OAuthHandler
from collections import Counter

consumer_key = <consumer_key>
consumer_secret = <consumer_secret>
access_token = <access_token>
access_secret = <access_secret>
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


def update_profile(api, cnt, writer, screenName, followerOf, followedBy):
    friendsList = []
    
    for friend in tweepy.Cursor(api, screen_name=screenName).items(cnt):
        identity = friend.id
        name = friend.name
        screen_name = friend.screen_name
        friendsList.append(screen_name)
        location = friend.location
        followers_count = friend.followers_count
        friends_count = friend.friends_count
        writer.writerow([identity, name, screen_name, location, followers_count, friends_count, followerOf, followedBy])
    
    return friendsList


with open("people_info.csv", "w") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["id", "name", "screen_name", "location", "followers_count", "friends_count", "follower_of", "followed_by"])
    friendsList = update_profile(api.friends, 100, writer, <screen_name>, None, <screen_name>)
    
    for friend in friendsList:
        update_profile(api.friends, 25, writer, friend, None, friend)
        update_profile(api.followers, 25, writer, friend, friend, None)
    
    followersList = update_profile(api.followers, 100, writer, <screen_name>, <screen_name>, None)
    
    for follower in followersList:
        update_profile(api.friends, 25, writer, follower, None, follower)
        update_profile(api.followers, 25, writer, follower, follower, None)
    

with open("node_pair.txt", "w") as outputFile:
    df = pd.read_csv("people_info.csv")
    col1 = 6
    col2 = 7
    col3 = 2
    rows, cols = df.shape
    
    for i in range(rows):
        
        if df.iat[i, col1] != df.iat[i, col1]:
            a = df.iat[i, col2]
            b = df.iat[i, col3]
        else:
            a = df.iat[i, col3]
            b = df.iat[i, col1]
        
        nodePair = "%s \t %s\n" % (a, b)
        outputFile.write(nodePair)


with open("node_list.txt", "w") as outputFile:
    df = pd.read_csv("people_info.csv")
    nodeList = df.screen_name.unique()
    
    for i in range(len(nodeList)):
        outputFile.write(nodeList[i])
        outputFile.write("\n")


with open("node_list.txt", "r") as outputFile:
    screenNameList = outputFile.read().split()


with open("node_map.txt", "w") as outputFile:
    df = pd.read_csv("people_info.csv")
    nodeList = df.name.unique()
    
    for i in range(len(nodeList)):
        nodeMap = "%s \t %s\n" % (screenNameList[i], nodeList[i])
        outputFile.write(nodeMap)

attributes = pd.read_excel("Hashtags_tags.xlsx", header=None)
attributes = attributes.T
attributeList = attributes.values.tolist()

for i in range(len(attributeList[0])):
    if not str(attributeList[0][i]).startswith('#'):
        attributeList[0][i] = '@'+str(attributeList[0][i])

with open("node_list.txt", "r") as inputFile:
    users = inputFile.read().splitlines()


with open("Extracted_Attributes1.txt", "r") as attrFile:
    attributes = attrFile.read().splitlines()

cnt = Counter(attributes)
attributeList = [k for k, v in cnt.items() if v > 1]


df = pd.DataFrame(columns=attributeList)
df = df.reindex(users, fill_value=0)


tweets = pd.read_csv("Tweets.csv", header=None)
rows, cols = tweets.shape

for i in range(rows):
    user = tweets.iat[i, 0]
    tweet = tweets.iat[i, 1]
    attributes = list(set(attributeList) & set(tweet.split()))
    
    for atr in attributes:
        value = df.loc[user, atr]
        df.loc[user,atr] = (value + 1)

df.to_csv("input_data.csv")

data = pd.read_csv("input_data.csv", index_col=0)
count = data.astype(bool).sum(axis=0)
dropList = []

for i in range(len(count)):
    if count[i] <= 1:
        dropList.append(i)

columns = data.columns
dropList = [columns[i] for i in dropList]
data.drop(columns=dropList, inplace=True)
data.to_csv("input_data_new.csv")
