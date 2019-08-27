from requests_oauthlib import OAuth1Session
import json

def authentication():

    keys = {
        "CK": "LzaQUb4iBsmRzNQsSLQ2qvfR6",
        "CS": "RS2mWhCrF5RH2bl7acvx0oTQjE1OBNaJ8EECipdWqDtr7dHm44",
        "AT": "706671194389393409-9CgeVYb5evzCNH8iTVaBW8xVitucloM",
        "AS": "c9cQ2RMJqofG8irPcbwRVBx3hYBkAhSVToOpXLGyPO1Od",
           }

    twitter = OAuth1Session(keys["CK"], keys["CS"], keys["AT"], keys["AS"])
    url = "https://api.twitter.com/1.1/trends/place.json"
    params = {"id": "23424856"}
    s = twitter.get(url, params=params)
    timeline = json.loads(s.text)
    #print(timeline)

    for tweet in timeline[0]['trends']:
        s = tweet['name']
        t = tweet['tweet_volume']
        print(s, t)

authentication()