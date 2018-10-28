import sqlite3
from flask import Flask
from flask import render_template, request, redirect, url_for
from extractor import extractor
import requests
import json
from math import inf
app = Flask(__name__)

@app.route('/manifest.json') 
def manifest():
	return redirect(url_for('static', filename='manifest.json'))

@app.route('/')
def index():
    return redirect(url_for('trending'))

@app.route('/trending')
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
    
        conn = sqlite3.connect('db.sqlite')
        c = conn.cursor()
        c.execute("SELECT * FROM politicians")
        politicians = c.fetchall()

        contains = []

        for politician in politicians:
            if data['content'].count(politician[1]) > 0 or data['title'].count(politician[1]) > 0:
                contains.append(politician[1])

        return render_template('analyse_result.html', url = request.form['url'], title = data['title'],  dtitle = j['title']["decision"], dcontent = j['content']["decision"], contains = contains)
    return 'ERROR : URL Not Supported!'

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/do-search', methods=['POST'])
def do_search():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    #c.execute('SELECT * from `articles` WHERE title LIKE %%%s%%' % request.form['term'])
    #data = c.fetchall()
    c.execute('SELECT `articles`.*, `fakebox`.`dtitle`, `fakebox`.`dcontent`, `mediahouse`.`mhname`, `sentiments`.`sentscore` \
    from `articles`, `fakebox`, `mediahouse`, `sentiments` WHERE LOWER(`articles`.`title`) LIKE \'%%%s%%\' AND `articles`.`article_id` = `fakebox`.`article_id` AND `articles`.`mhid` = `mediahouse`.`mhid` AND `articles`.`article_id` = `sentiments`.`article_id` AND `sentiments`.`pid` = 0;' % request.form['term'].lower() )

    #c.execute('SELECT `articles`.`article_id`, `articles`.`url`, `articles`.`title`, `articles`.`mhid`, `fakebox`.`dtitle`, `fakebox`.`dcontent`, `mediahouse`.`mhname` \
    #from `articles`, `fakebox`, `mediahouse` WHERE LOWER(`articles`.`title`) LIKE \'%%%s%%\' AND `articles`.`article_id` = `fakebox`.`article_id` AND `articles`.`mhid` = `mediahouse`.`mhid`;' % request.form['term'] )
    articles = c.fetchall()
    most_negative = +inf
    most_negative_url = None
    most_negative_name = None

    most_positive = -inf
    most_positive_url = None
    most_positive_name = None
    
    for article in articles:
        sentiment = article[-1]
        if article[5]=='bias' or article[6]=='bias':
            if sentiment < most_negative:
                most_negative = sentiment
                most_negative_url = article[1]
                most_negative_name = article[2]
            if sentiment > most_positive:
                most_positive = sentiment
                most_positive_url = article[1]
                most_positive_name = article[2]

    #return str(most_negative_aid) + " " + str(most_positive_aid)     

    '''
    if most_negative > 0.05:
       most_negative_url = None

    if most_positive < 0.05:
        most_positive_url = None'''
   
    ''' for article in articles:
        best_pairing = None
        c.execute("SELECT `sentscore` FROM `sentiments` WHERE article_id=? AND pid=0", article[0])
        sentiment = c.fetchall()[0][2]
        if sentiment >= 0.05:
            category = '+'
        else
            category = '-'
    '''    
    '''for i, article2 in enumerate(aritcles):
            c.execute("SELECT `sentscore` FROM `sentiments` WHERE article_id=? AND pid=0", article2[0])
            sentiment = c.fetchall()[0][2]
            if sentiment >= 0.05:
                category = '+'
            else
                category = '-'
    '''    
            
            

    contains_list = []
    for article in articles:
        c.execute('SELECT `sentiments`.`pid`, `politicians`.`pname` FROM `sentiments`, `politicians` WHERE `sentiments`.`article_id`=%d AND `sentiments`.`pid` = `politicians`.`pid`;' %
        article[0])
        contains_list.append(c.fetchall())

    return render_template('search_result.html', var = articles , contains = contains_list, most_negative = most_negative_url, most_positive = most_positive_url,
    most_negative_name = most_negative_name, most_positive_name = most_positive_name)

app.run(host="0.0.0.0", debug=True)