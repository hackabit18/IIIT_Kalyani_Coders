import sqlite3
from flask import Flask
from flask import render_template, request, redirect, url_for
from extractor import extractor
import requests
import json
app = Flask(__name__)

@app.route('/manifest.json') 
def manifest():
	return redirect(url_for('static', filename='manifest.json'))

@app.route('/')
def trending():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('SELECT `articles`.*, `fakebox`.`dtitle`, `fakebox`.`dcontent`, `mediahouse`.`mhname` \
    from `articles`, `fakebox`, `mediahouse` WHERE `articles`.`article_id` = `fakebox`.`article_id` AND `articles`.`mhid` = `mediahouse`.`mhid`;')
    articles = c.fetchall()
    contains_list = []
    for article in articles:
        c.execute('SELECT `sentiments`.`pid`, `politicians`.`pname` FROM `sentiments`, `politicians` WHERE `sentiments`.`article_id`=%d AND `sentiments`.`pid` = `politicians`.`pid`;' %
        article[0])
        contains_list.append(c.fetchall())

    return render_template('trending.html', var = articles , contains = contains_list)

@app.route('/mediahouse/<int:mhid>')
def mediahouse(mhid):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("SELECT * FROM mediahouse WHERE mhid = %d" % mhid)
    d  = c.fetchall()
    _, mhname, mhurl = d[0]
    c.execute("SELECT * FROM `politicians`")
    politicians = c.fetchall()
    positivefor = []
    negativefor = []
    insufficientfor = []
    c.execute("SELECT count(*) from articles WHERE mhid = %d" % mhid)
    article_count = c.fetchall()[0][0]
    for pid, pname, pparty in politicians:
        c.execute("SELECT * FROM `sentiments` WHERE `mhid` = ? and `pid` = ?", (mhid, pid))
        rows = c.fetchall()
        negatives = 0
        positives = 0
        if len(rows) == 0:
            insufficientfor.append((pid, pname))
        else:
            for row in rows:
                if row[2] >= 0.05:
                    positives += 1
                else:
                    negatives += 1
            if positives >= negatives:
                positivefor.append((pid, pname, positives * 100 / (positives + negatives)))
            else:
                negativefor.append((pid, pname, negatives * 100 / (positives + negatives)))
    #return str(positivefor) + "\n\n" + str(negativefor) + "\n\n" + str(insufficientfor)
    return render_template("mediahouse.html", positivefor = positivefor, negativefor = negativefor, insufficientfor = insufficientfor
    , mhname = mhname, mhurl = mhurl,  article_count =  article_count)


@app.route('/analyse')
def analyse():
    return render_template('analyse.html')

@app.route('/do-analysis', methods=['POST'])
def do_analysis():
    data = extractor(request.form['url'])
    if data:
        r = requests.post("http://localhost:8080/fakebox/check", data={
            "url" : data['url'],
            "title": data['title'],
	        "content": data['content']
        })
        j = json.loads(r.text)
        return render_template('analyse_result.html', url = request.form['url'], title = data['title'],  dtitle = j['title']["decision"], dcontent = j['content']["decision"])
    return 'ERROR : URL Not Supported!'

app.run(host="0.0.0.0", debug=True)