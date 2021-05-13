import feedparser
from flask import Flask, render_template, request


app = Flask(__name__)


RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'lifehacker': 'https://lifehacker.com/rss',
            'wired': 'https://www.wired.com/feed/rss',
            'hackernoon': 'https://hackernoon.com/feed',
            'darkhacker': 'http://feeds.feedburner.com/Darkhackerworld',
            'hackaday': 'https://hackaday.com/blog/feed/',
            'howtogeek': 'http://feeds.howtogeek.com/HowToGeek'
            }


@app.route("/")
def get_news():

    query = request.args.get('publication')

    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'

    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])


    return render_template("home.html", articles=feed['entries'])


if __name__ == "__main__":
    app.run(debug=True)
