from requests_oauthlib import OAuth1Session
import json

def authentication():

    keys = {
        "CK": "",
        "CS": "",
        "AT": "",
        "AS": "",
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
