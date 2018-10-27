from requests_html import HTMLSession
from pprint import pprint
'''
session = HTMLSession()

url = input()
#url = 'https://www.ndtv.com/india-news/bjp-standing-like-a-rock-with-devotees-says-amit-shah-in-kerala-after-over-2-000-arrested-for-protes-1938485?pfrom=home-topscroll'

r = session.get(url)

span = r.html.find("div.ins_headline span")[0]
title = span.text

content_div = r.html.find("[itemprop=articleBody]")[0]
content = content_div.text

pprint()'''

def extractor(url):
    if not url.startswith('https://www.ndtv.com/'):
        return None
        
    session = HTMLSession()
    r = session.get(url)

    span = r.html.find("div.ins_headline span")[0]
    title = span.text

    content_div = r.html.find("[itemprop=articleBody]")[0]
    content = content_div.text

    return {
        "url" : url,
        "title" : title,
        "content" : content
    }