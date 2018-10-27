import requests
import json
import sqlite3
from textblob import TextBlob

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

c.execute("SELECT max(article_id) FROM articles")
last_articleid = c.fetchall()[0][0]

url = "https://thewire.in/media/cobrapost-sting-big-media-houses-say-yes-to-hindutva-black-money-paid-news"
title = "Cobrapost Sting: Big Media Houses Say Yes to Hindutva, Black Money, Paid News"
content = """
New Delhi: Nearly two months after Cobrapost first reported how some media houses were prepared to strike business deals to promote the Hindutva agenda and help polarise voters in the run up to the 2019 elections, the website has released a second batch of video recordings shot surreptitiously by an undercover reporter that shows managers and owners of some of the largest newspapers and TV channels succumbing to the same package of Hindutva advertorials.

Cobrapost said on Friday that the recordings it made showed how some two dozen news organisations were willing to “not only cause communal disharmony among the citizens but also tilt the electoral outcome in favour of a particular party” for a price.

The only two media houses whose representatives refused the undercover reporter’s proposals were the Bengali newspapers Bartaman and Dainik Sambad.

In what is likely to alarm the finance ministry and the income tax department, several of the media houses – including, in some cases, proprietors like Vineet Jain of the Times Group – have been recorded discussing ways in which proposed transactions running into hundreds of crores of rupees could be conducted using cash, i.e. black money.

The Times Group owns the Times Now channel, the Times of India and several other media platforms. The ease with which Jain discusses ways in which the undercover reporter could pay the company using black money by routing those payments through other business houses and families is hard to reconcile with Times Now’s campaigns in favour of demonetisation – which Prime Minister Narendra Modi had said was needed in order to deal with black money.

For the sting, an undercover journalist, Pushp Sharma, posed as “Acharya Atal”, a man who identified himself as a representative of an unnamed “sangathan”, or organisation, but who gave the impression that he was a member of or close to the Nagpur-based Rashtriya Swayamsewak Sangh (RSS). In the recordings the website put up on YouTube on Friday afternoon, Acharya Atal can be heard trying to strike deals with media house executives involving the promotion of a Hindutva agenda through advertorials – paid-for content – that would run on their newspapers, radio stations, TV channels and websites.

Vineet Jain of Times Group 

The biggest name to be stung by Cobrapost was Times Group owner and managing director Vineet Jain. In a number of videotaped conversations, Jain and the group’s executive president, Sanjeev Shah, can be seen and heard discussing the proposed deal in which Acharya Atal said he would pay Rs 500 crore in exchange for advertorials and events that that would be presented as programming on Krishna and the Bhagvad Gita but which would serve as a cover for Hindutva and its political agenda.

In one of the meetings, Jain and Shah offer guidance to the undercover journalist on how to make payments in cash even though they said the Times group itself had no use for cash.

“We found them naming some big corporate houses which could help make black money squeaky clean,” Cobrapost said.

It added that while Vineet Jain said, “Aur bhi businessmen honge jo humein cheque denge aap unhe cash de do” (There are other businessmen who would give us cheque against the cash you may give them), his aide Shah elaborated on this to the undercover journalist saying: “Who will take that from him in Delhi suppose if Goenka says I want it in Ahmedabad so that I Angadiya will have contact in Ahmedabad where they will exchange in number on a note or whatever.”

Incidentally, Rs 500 crore is equal to a little more than 5% of the total revenue of Rs 9,976 crore that the Times group earned in 2017.

In a response emailed to The Wire on May 26, a TOI group representative, Mritunjay Kataria, said, “We only made a marketing offer to reel [the Cobrapost reporter] in to reveal his antecedents. We categorically state we do not deal in cash in any manner, all large business dealings happen in legal manner though banking channels. Our statements made in this context were misquoted/misrepresented.”

Kataria also said his company was aware of the “nefarious” activity of the Cobrapost reporter and that its senior functionaries had actually strung him along as part of a “reverse sting” in an effort to “reel him in”.

Kalli Purie of India Today group 

In his meeting with Kalli Purie, vice-chairperson of the India Today group, Cobrapost’s undercover journalist spoke about using Krishna and the Bhagvad Gita to promote Hindutva since Ram and Ayodhya had become controversial. He said the ‘sangathan’ would make use of the Krishna messaging the India Today group would put out to promote Hindutva among the wider public as part of its “infield activities”. The reporter also spoke about translating the campaign for his “political gains” and even said that he should not be held accountable later for polarisation.

Purie indicated she was agreeable to the idea but added that “if you are doing some infield activities that we don’t agree with editorially, we will be criticising you”. She urged ‘Acharya Atal’ not to resort to polarising activities but when he said the course of the election campaign may not leave him any option, his insistence did not become a deal breaker.

Pushp Sharma had earlier met TV Today’s chief revenue officer, Rahul Kumar Shaw, who had conveyed to  him his own support for the sangathan’s agenda. “I must tell you, I am very very pro, very pro to the government”. Soon after the meeting with Kalli Purie, Shaw sent an email proposing a Rs 275 crore advertising campaign – an astonishing amount for what was officially going to be described as promotion of the Bhagvad Gita. The value placed on this one campaign alone was 20% of the total revenues earned by the India Today group in 2017.

"""

c.execute("SELECT * FROM mediahouse")
media_houses = c.fetchall()

article_mh = -1

for mh in media_houses:
    if url.startswith(mh[2]):
        article_mh = mh[0]
        break

c.execute("INSERT INTO `articles` VALUES (?, ?, ?, ?, ?)", (last_articleid + 1,
url, title, content, article_mh))

r = requests.post("http://localhost:8080/fakebox/check", data={
    "url" : url,
    "title": title,
    "content": content
})

response_json = json.loads(r.text)

decision_title = response_json['title']['decision']
decision_content = response_json['content']['decision']
score_title = response_json['title']['score']
score_content = response_json['content']['score']

c.execute("INSERT INTO `fakebox` VALUES (?, ?, ?, ?, ?)", (last_articleid + 1,
decision_title, score_title, decision_content, score_content))

tb = TextBlob(content)
polarity = tb.sentiment.polarity

c.execute("INSERT INTO `sentiments` VALUES (?, ?, ?, ?)", (last_articleid + 1,
0, polarity, article_mh))

c.execute("SELECT * FROM politicians")
politicians = c.fetchall()

contains = []
for politician in politicians:
    if content.count(politician[1]) > 0 or title.count(politician[1]) > 0:
        contains.append(politician[0])

for pid in contains:
    c.execute("INSERT INTO `sentiments` VALUES (?, ?, ?, ?)", (last_articleid + 1, pid, polarity, article_mh))

conn.commit()

conn.close()






