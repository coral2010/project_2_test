# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import api_key
import requests
import tweepy
import json
from config import consumer_key, consumer_secret, access_token, access_token_secret

def weather_scrape():

    api_key = api_key.api_key

    location = "Yosemite Valley"

    url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&appid=" + api_key + "&q=" + location

    weather = requests.get(url).json()

    todays_temp = weather["main"]["temp"]
    todays_humid = weather["main"]["humidity"]

return todays_temp, todays_humid

def twitter_scrape():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target_user = "YosemiteNPS"

    user_tweets_only = api.user_timeline(target_user, count=1, result_type="recent")
    user_tweets = user_tweets_only[0]["text"]

return user_tweets

def news_scrape():
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.nps.gov/yose/learn/news/newsreleases.htm'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Article Title
    news_title = soup.find("h3", class_="ListingResults-title").text

    # Article Date
    article_date = soup.find("div", class_="ListingMeta").text

    # Link to full article
    results = soup.find("li", class_="ListingList-item ListingResults-item")
    news_link = results.find("a")["href"]
    split_url = urlsplit(url)
    full_news_link = split_url.scheme + "://" + split_url.netloc + news_link

    # Article summary
    article_text = soup.find("p", class_="ListingResults-description").text

return news_title, article_date, full_news_link, article_text