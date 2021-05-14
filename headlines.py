import feedparser
from flask import Flask, render_template, request
import json
import urllib.request


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
    weather = get_weather("Republic Of India,IN")

    return render_template("home.html", articles=feed['entries'], weather=weather)


def get_weather(query):

    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b8140f6c81b641f99751926b0d964f9f'
    query = urllib.request.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                    "temperature": parsed["main"]["temp"],
                    "city": parsed["name"]
                    }

    return weather


if __name__ == "__main__":
    app.run(debug=True)
