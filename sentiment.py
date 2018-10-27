from textblob import TextBlob 
import json
import sqlite3
from textblob.sentiments import NaiveBayesAnalyzer

with open("news.json", "r") as f:
    data = json.load(f)

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

c.execute("SELECT * FROM `politicians`")

politicians = c.fetchall()

aid = 0
'''for article in data["articles"]:
    s = 0
    l = article['content'].split('.')
    for line in l:
        t = TextBlob(line, analyzer=NaiveBayesAnalyzer())
        s += t.sentiment.polarity
    s = s / len(l)
    print(s)

print("\n\nNormal\n\n")'''
for article in data["articles"]:
    print(TextBlob(article['content'], analyzer=NaiveBayesAnalyzer()).sentiment)
    #t = TextBlob(article['content'])
    #polarity = t.sentiment.polarity
    #for pid, pname, pparty in politicians:
        #if (article['content'].count(pname) > 0):
            #c.execute("INSERT INTO `sentiments` VALUES (?, ?, ?)", (aid, pname, polarity))
    #aid += 1

conn.commit()

conn.close()