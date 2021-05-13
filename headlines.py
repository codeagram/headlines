import feedparser
from flask import Flask, render_template


app = Flask(__name__)


RSS_FEEDS = {'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
            'LifeHacker': 'https://lifehacker.com/rss',
            'Wired': 'https://www.wired.com/feed/rss',
            'HackerNoon': 'https://hackernoon.com/feed',
            'DarkHacker': 'http://feeds.feedburner.com/Darkhackerworld',
            'HackADay': 'https://hackaday.com/blog/feed/',
            'HowToGeek': 'http://feeds.howtogeek.com/HowToGeek'
            }


@app.route("/")
@app.route("/<publication>")
def get_news(publication='BBC'):

    feed = feedparser.parse(RSS_FEEDS[publication])


    return render_template("home.html", articles=feed['entries'])


if __name__ == "__main__":
    app.run(debug=True)
