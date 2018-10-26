from textblob import TextBlob 
import json
import sqlite3

with open("news.json", "r") as f:
    data = json.load(f)

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

c.execute("SELECT * FROM `politicians`")

politicians = c.fetchall()

aid = 0
for article in data["articles"]:
    t = TextBlob(article['content'])
    polarity = t.sentiment.polarity
    for pid, pname, pparty in politicians:
        if (article['content'].count(pname) > 0):
            c.execute("INSERT INTO `sentiments` VALUES (?, ?, ?)", (aid, pname, polarity))
    aid += 1

conn.commit()

conn.close()