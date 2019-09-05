from requests_oauthlib import OAuth1Session
import json
import codecs
import schedule
import time
import calendar
from datetime import datetime
import tweet_info

Flag = 0
last = datetime(2017, 11, 12, 9, 55, 28)

keys = {
        "CK": "LzaQUb4iBsmRzNQsSLQ2qvfR6",
        "CS": "RS2mWhCrF5RH2bl7acvx0oTQjE1OBNaJ8EECipdWqDtr7dHm44",
        "AT": "706671194389393409-9CgeVYb5evzCNH8iTVaBW8xVitucloM",
        "AS": "c9cQ2RMJqofG8irPcbwRVBx3hYBkAhSVToOpXLGyPO1Od",
     }

filename = "newtweet.text"


def initilize(timeline):
    global last
    i = 0
    f = codecs.open(filename, "w", "utf-8")
    for tweet in timeline:
        t = time_change(tweet)
        s = tweet_info.TweetInfo(t, tweet['user']['name'], tweet['text'])

        print_tweet(f, s)

        if i == 0:
            last = t
            i += 1
    f.close()


def update(timeline):
    global last
    i = 0
    f = codecs.open(filename, "a", "utf-8")
    for tweet in timeline:
        t = time_change(tweet)
        s = tweet_info.TweetInfo(t, tweet['user']['name'], tweet['text'])

        if i == 0:
            last2 = t
            i += 1

        if last < t:
            i += 1
            f.seek(0, 0)
            print("test")
            print_tweet(f, s, "追記")

    f.close()
    last = last2

    if 2 > i:
        print("最新のツイートはありません\n")


def print_tweet(file_stream, tweet: tweet_info.TweetInfo, remark: str = ""):
    file_stream.write(tweet.to_string() + remark)
    print(tweet.to_string() + remark)


def get_request_twitter():

    sess = OAuth1Session(keys["CK"], keys["CS"], keys["AT"], keys["AS"])

    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

    params = {"count": 30,
              "include_entities": True,
              "exclude_replies": 1,
              }

    request = sess.get(url, params=params)
    return request


def print_rest_request_count(req):
    limit = req.headers['x-rate-limit-remaining']  # リクエスト可能残数の取得
    m = int((int(req.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.now().timetuple())) / 60)
    print("リクエスト可能残数: " + limit)
    print('リクエスト可能残数リセットまでの時間:  %s分' % m,"\n")


def main(print_tweet_function):
    request = get_request_twitter()
    print_rest_request_count(request)
    if check_valid_api(request):
        timeline = json.loads(request.text)
        print_tweet_function(timeline)
    else:
        print("Failed: %d" % request.status_code)


def check_valid_api(req):
    if req.status_code == 200:
        return True
    else:
        return False


def time_change(tweet):
    time_utc = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    japan_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return japan_time


def test():
    return main(update)


if __name__ == '__main__':
    main(initilize)
    schedule.every(5).minutes.do(test)
    while True:
        schedule.run_pending()
        time.sleep(1)