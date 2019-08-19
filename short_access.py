from requests_oauthlib import OAuth1Session
import json
import codecs
import schedule
import time
import calendar
from datetime import datetime

Flag = 0
last = datetime(2017, 11, 12, 9, 55, 28)

keys = {
        "CK": "LzaQUb4iBsmRzNQsSLQ2qvfR6",
        "CS": "RS2mWhCrF5RH2bl7acvx0oTQjE1OBNaJ8EECipdWqDtr7dHm44",
        "AT": "706671194389393409-9CgeVYb5evzCNH8iTVaBW8xVitucloM",
        "AS": "c9cQ2RMJqofG8irPcbwRVBx3hYBkAhSVToOpXLGyPO1Od",
     }

filename = "newtweet.text"

def mai():
    global Flag, last
    i = 0

    sess = OAuth1Session(keys["CK"], keys["CS"], keys["AT"], keys["AS"])

    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

    params = {"count": 30,
              "include_entities": True,
              "exclude_replies": 1,
              }

    req = sess.get(url, params=params)

    timeline = json.loads(req.text)

    limit = req.headers['x-rate-limit-remaining']  # リクエスト可能残数の取得
    m = int((int(req.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.now().timetuple())) / 60)
    print("リクエスト可能残数: " + limit)
    print('リクエスト可能残数リセットまでの時間:  %s分' % m,"\n")

    if req.status_code == 200:  # OKの場合
        if Flag == 0:
            f = codecs.open(filename, "w", "utf-8")
            for tweet in timeline:
                t = time_change(tweet)
                s = [t, tweet['user']['name'], tweet['text']]


                f.write(s[1])
                f.write('   ')
                f.write(s[0])
                f.write("\n")
                f.write(s[2])
                f.write("\n" * 2)

                print(s[1], s[0], "\n", s[2], "\n" * 2)

                if i == 0:
                    last = t
                    i += 1
            f.close()

        else:
            f = codecs.open(filename, "a", "utf-8")
            for tweet in timeline:
                t = time_change(tweet)
                s = [t, tweet['user']['name'], tweet['text']]

                if i == 0:
                    last2 = t
                    i += 1

                if last < t:
                    i += 1
                    f.seek(0)
                    f.write(s[1])
                    f.write('   ')
                    f.write(s[0])
                    f.write("追記")
                    f.write("\n")
                    f.write(s[2])
                    f.write("\n" * 4)
                    print(s[1], s[0], "追記", "\n", s[2], "\n" * 2)

            f.close()
            last = last2

            if 2 > i:
                print("最新のツイートはありません\n")

    else:
        print("Failed: %d" % req.status_code)

    Flag += 1
    print(last, "last")

def time_change(tweet):
    time_utc = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    japan_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return japan_time


if __name__ == '__main__':
    mai()
    schedule.every(1).minutes.do(mai)
    while True:
        schedule.run_pending()
        time.sleep(1)