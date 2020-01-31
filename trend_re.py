from requests_oauthlib import OAuth1Session
import json
import time
from datetime import  datetime
import trend_info
import calendar


keys = {
            "CK": "",
            "CS": "",
            "AT": "",
            "AS": "",
        }

class TweetInfo:
    def __init__(self, message, volumu):
        self.__message = message
        self.__volume = volumu


    def get_request_twitter():
        
        twitter = OAuth1Session(keys["CK"], keys["CS"], keys["AT"], keys["AS"])
        url = "https://api.twitter.com/1.1/trends/place.json"
        params = {"id": "23424856"} #日本の地名コード
        req = twitter.get(url, params=params)
        return req

    def print_rest_request_count(req):
        limit = req.headers['x-rate-limit-remaining']  # リクエスト可能残数の取得
        m = int((int(req.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.now().timetuple())) / 60)
        print("リクエスト可能残数: " + limit)
        print('リクエスト可能残数リセットまでの時間:  %s分' % m,"\n")

    def check_valid_api(req):
        if req.status_code == 200:
            return True
        else:
            return False

    def main(print_tweet_function):
        request = .get_request_twitter()
        print_rest_request_count(request)
        if check_valid_api(request):
            timeline = json.loads(request.text)
            print_tweet_function(timeline)
        else:
            print("Failed: %d" % request.status_code)
