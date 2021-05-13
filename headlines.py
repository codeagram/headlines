import feedparser
from flask import Flask


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
    print(publication)
    first_article = feed['entries'][0]

    return """\
            <html>
                <body>
                    <h1>Head Lines</h1>
                    <b>{0}</b><br>
                    <i>{1}</i><br>
                    <p>{2}</p><br>
                </body>
            </html>
            """.format( first_article.get("title"),
                first_article.get("published"),
                first_article.get("summary"))


if __name__ == "__main__":
    app.run(debug=True)
