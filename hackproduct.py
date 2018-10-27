import sqlite3
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def trending():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('SELECT `articles`.*, `fakebox`.`dtitle`, `fakebox`.`dcontent`, `mediahouse`.`mhname` \
    from `articles`, `fakebox`, `mediahouse` WHERE `articles`.`article_id` = `fakebox`.`article_id` AND `articles`.`mhid` = `mediahouse`.`mhid`;')
    return render_template('trending.html', var = c.fetchall())

@app.route('/mediahouse/<int:mhid>')
def mediahouse(mhid):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM `politicians`")
    politicians = c.fetchall()
    for pid, pname, pparty in politicians:
        

app.run(host="0.0.0.0", debug=True)