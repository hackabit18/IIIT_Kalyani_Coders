from textblob import TextBlob 
import json
import sqlite3

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()
c.execute('SELECT article_id, url, title, content, mhid FROM articles')
articles = c.fetchall()

for article in articles:
    t = TextBlob(article[3])
    c.execute('INSERT INTO `sentiments` VALUES (?, ?, ?, ?)', (article[0], 0, t.sentiment.polarity, article[-1] ))

conn.commit()
conn.close()