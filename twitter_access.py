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
        "CK": "",
        "CS": "",
        "AT": "-",
        "AS": "",
     }

filename = "tweet2.text"


def main():
    global Flag, last

    sess = OAuth1Session(keys["CK"], keys["CS"], keys["AT"], keys["AS"])

    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

    params = {"count": 10,
            "include_entities": True,
            "exclude_replies": 1,
             }

    req = sess.get(url, params=params)

    timeline = json.loads(req.text)

    limit = req.headers['x-rate-limit-remaining']  # リクエスト可能残数の取得
    m = int((int(req.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.now().timetuple())) / 60)
    print("リクエスト可能残数: " + limit)
    print('リクエスト可能残数リセットまでの時間:  %s分' % m)

    f = codecs.open(filename, "w", "utf-8")

    i = 0

    if req.status_code == 200:  # OKの場合
        for tweet in timeline:
            time_utc = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            unix_time = calendar.timegm(time_utc)
            time_local = time.localtime(unix_time)
            japan_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            s = [japan_time, tweet['user']['name'], tweet['text']]

            f.write(s[1])
            f.write('   ')
            f.write(s[0])
            f.write("\n")
            f.write(s[2])
            f.write("\n" * 2)

            print(s[1],  s[0], "\n", s[2], "\n"*2)

            if i == 0:
                last = japan_time
                i += 1

    else:
        print("Failed: %d" % req.status_code)

    f.close()
    Flag += 1

def mai():
    global Flag, last
    i = 0
    f = codecs.open(filename, "a", "utf-8")

    sess = OAuth1Session(keys["CK"], keys["CS"], keys["AT"], keys["AS"])

    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

    params = {"count": 10,
              "include_entities": True,
              "exclude_replies": 1,
              }

    req = sess.get(url, params=params)

    timeline = json.loads(req.text)

    if req.status_code == 200:  # OKの場合

        for tweet in timeline:
            time_utc = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            unix_time = calendar.timegm(time_utc)
            time_local = time.localtime(unix_time)
            japan_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            s = [japan_time,tweet['user']['name'], tweet['text']]

            if i == 0:
                last2 = japan_time
                i += 1

            if last < japan_time:
                i += 1
                f.write(s[1])
                f.write('   ')
                f.write(s[0])
                f.write("追記")
                f.write("\n")
                f.write(s[2])
                f.write("\n" * 4)
                print(s[1], s[0], "追記", "\n", s[2], "\n" * 2)

    else:
        print("Failed: %d" % req.status_code)

    f.close()
    last = last2

    if 2 > i:
        print("最新のツイートはありません")

    Flag += 1
    print(last, "last")


main()
schedule.every(5).minutes.do(mai)
while True:
    schedule.run_pending()
    time.sleep(1)
