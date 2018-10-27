import sqlite3
import json
import requests
from pprint import pprint

conn = sqlite3.connect("db.sqlite")
c = conn.cursor()
#c.execute("CREATE TABLE `articles` ( `article_id` INT NOT NULL , `url` VARCHAR(400) NOT NULL , `title` VARCHAR(1000) NOT NULL , `content` TEXT NOT NULL , PRIMARY KEY (`article_id`));")


with open("news.json", "r") as f:
    data = json.load(f)

aid = 0
for article in data["articles"]:
    c.execute("INSERT INTO `articles` VALUES (?, ?, ?, ?)", (aid, article['url'], article['title'], article['content']))
    aid += 1

'''c.execute("""
CREATE TABLE `fakebox` 
( `article_id` INT NOT NULL , `dtitle` VARCHAR(100) NOT NULL , `stitle` DECIMAL(1000) NOT NULL , `dcontent` VARCHAR(100) NOT NULL , `scontent` DECIMAL NOT NULL , PRIMARY KEY (`article_id`)); 
""")'''

aid = 0
print("Perfoming FakeBox Analysis")
for article in data["articles"]:
    r = requests.post("http://localhost:8080/fakebox/check", data={
    "url" : article['url'],
    "title": article['title'],
	"content": article['content']
    })
    pprint(r.text)
    j = json.loads(r.text)
    c.execute("INSERT INTO `fakebox` VALUES (?, ?, ?, ?, ?)", (aid, j['title']["decision"], j['title']["score"], j['content']["decision"], j['content']["score"]))
    aid += 1
print("Done")

conn.commit()

conn.close()