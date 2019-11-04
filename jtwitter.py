import codecs

import json

import MeCab

filename = "a2.text"

i = 0
m = MeCab.Tagger('C:\Program Files (x86)\MeCab\dic\mecab-ipadic-neologd\seed')
f1 = codecs.open(filename, "w", "utf-8")

with open("/Users/Yamada Osamu/Desktop/twitter/json_2019-09-08.txt",encoding="utf-8") as f:

    while True:
        line = f.readline()
        if i == 10:
            break
        li = line[20:]
        dic = json.loads(li)
        print(dic["text"])
        f1.write(line[0:20]+ dic["text"] +"\n"*10 +m.parse(dic["text"]))
        print(line[0:20])
        i+=1
        print(i)

       
   

    