from requests_oauthlib import OAuth1Session
import json
import os
import urllib
import datetime, time
import codecs
import calendar

flag = 0

def authentication(ward):

    keys = {
        "CK": "",
        "CS": "",
        "AT": "",
        "AS": "",
           }

    twitter = OAuth1Session(keys["CK"], keys["CS"], keys["AT"], keys["AS"])

    url = "https://api.twitter.com/1.1/search/tweets.json"

    params = {'q': ward,
              'count': 10
              }

    req = twitter.get(url, params=params)

    return req


def get_target_ward(req):

    if req.status_code == 200:
        timeline = json.loads(req.text)
        limit = req.headers['x-rate-limit-remaining']  # リクエスト可能残数の取得
        m = int((int(req.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.datetime.now().timetuple())) / 60)
        print("リクエスト可能残数: " + limit)
        print('リクエスト可能残数リセットまでの時間:  %s分' % m)
        return timeline
    else:
        print("ERROR: %d" % req.status_code)



# 取得したツイートに画像があれば、その画像を取得する
def get_illustration(timeline, dir_name):
    global image
    global image_number
    image_number = 0

    if not os.path.isdir(dir_name): #mkdir_nameのディレクトリの確認
        os.mkdir(dir_name) #もしなかったら作

    for tweet in timeline['statuses']:
        try:
            media_list = tweet['extended_entities']['media']
            dt = time_change(tweet)
            for media in media_list:
                image = media['media_url']
                with open(dir_name + "/" + dt + os.path.basename(image), 'wb') as f:
                    img = urllib.request.urlopen(image).read()
                    f.write(img)
                image_number += 1
            print("%d" % image_number, "get tweet media")

        except KeyError:
            pass

        except:
            print("error")

def get_text(timeline, dir_name,text_name):

    f = codecs.open(dir_name +"/" + text_name, "w", "utf-8")
    for tweet in timeline['statuses']:
        dt = time_change(tweet)
        s = [dt,tweet['user']['name'], tweet['text']]

        f.write(s[1])
        f.write('   ')
        f.write(s[0])
        f.write("\n")
        f.write(s[2])
        f.write("\n" * 2)
    f.close()


def time_change(tweet):
    time_utc = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    japan_time = time.strftime("%Y-%m-%d %H%M%S", time_local)
    return japan_time


def main():
    dir_name = "search_tweet"
    text_name = "trend.text"
    ward = "スタバ"

    req = authentication(ward)
    timeline = get_target_ward(req)
    get_illustration(timeline, dir_name)
    get_text(timeline, dir_name,text_name)
