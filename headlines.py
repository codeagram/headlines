import feedparser
from flask import Flask, render_template, request
from flask import make_response
import datetime
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


DEFAULTS = {
            'publication': 'bbc',
            'city': 'Republic of India, IN',
            'currency_from': 'USD',
            'currency_to': 'INR',
        }


def get_value_with_fallback(key):

    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)

    return DEFAULTS[key]


@app.route("/")
def home():

    publication = get_value_with_fallback('publication')
    articles = get_news(publication)

    city = get_value_with_fallback("city")
    weather = get_weather(city)

    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback('currency_to')
    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(render_template('home.html',
                            articles=articles,
                            weather=weather,
                            currency_from=currency_from,
                            currency_to=currency_to,
                            rate=rate,
                            currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    return response



def get_news(query):

    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']

    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("Republic Of India,IN")

    return feed['entries']


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
                    "city": parsed["name"],
                    "country": parsed['sys']['country'],
                    }

    return weather


def get_rate(frm, to):

    CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=c0eeaf3397db44858777c334d894b53c"
    all_currency = urllib.request.urlopen(CURRENCY_URL).read()

    parsed = json.loads(all_currency)
    frm_rate = parsed['rates'].get(frm.upper())
    to_rate = parsed['rates'].get(to.upper())

    return (to_rate/frm_rate, parsed['rates'].keys())


if __name__ == "__main__":
    app.run(debug=True)
