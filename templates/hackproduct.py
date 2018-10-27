import sqlite3
from flask import Flask
app = Flask(__name__)

@app.route('/')
def trending():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM `articles`')
    return str(c.fetchall())