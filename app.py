from flask import Flask, render_template, redirect
from pymongo import MongoClient
import json
import yosemite_scraper

client = MongoClient('mongodb://localhost:27017/yosemite_db')

###############################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Home Route
#################################################

@app.route("/")
def form():
    return render_template('index.html', scraped_data=scraped_data)

# access manually to re-scrape data and put into mongodb
@app.route("/scrape_data")
def scraped_data():
    print('INITIALIZING DATA SCRAPE FOR YOSEMITE NATIONAL PARK')
    print('-------------------------------------------------------')
    yosemite_scraper.economic_benefits()
    yosemite_scraper.post()
    yosemite_scraper.twitter()
    yosemite_scraper.news()
    yosemite_scraper.weather()
    yosemite_scraper.trail_table()
    print('SCRAPING COMPLETED')
    print('-------------------------------------------------------')
    return redirect("/", code=302)

#Each scraped collection gets its own route. Route is queried specifically for its specific plots
@app.route("/economic_benefits")
def economic_benefits():
    results = list(client.yosemite_db.economic_benefits.find())
    for result in results:
        del(result['_id'])
    return json.dumps(results)

@app.route("/post")
def post():
    results = list(client.yosemite_db.post.find())
    for result in results:
        del(result['_id'])
    return json.dumps(results)

@app.route("/twitter")
def twitter():
    results = list(client.yosemite_db.twitter.find())
    for result in results:
        del(result['_id'])
    return json.dumps(results)

@app.route("/news")
def news():
    results = list(client.yosemite_db.news.find())
    for result in results:
        del(result['_id'])
    return json.dumps(results)

@app.route("/weather")
def weather():
    results = list(client.yosemite_db.weather.find())
    for result in results:
        del(result['_id'])
    return json.dumps(results)

@app.route("/trail_table")
def trail_table():
    results = list(client.yosemite_db.trail_table.find())
    for result in results:
        del(result['_id'])
    return json.dumps(results)

@app.route("/annual_visitors")
def annual_visitors():
    results = list(client.yosemite_db.annual_visitors.find())
    for result in results:
        del(result['_id'])
    return json.dumps(results)

@app.route("/entrances")
def entrances():
    results = list(client.yosemite_db.entrances.find())
    for result in results:
        del(result['_id'])
    return json.dumps(results)

@app.route("/traffic_counts")
def traffic_counts():
    results = list(client.yosemite_db.traffic_counts.find())
    for result in results:
        del(result['_id'])
    return json.dumps(results)
    
if __name__ == '__main__':    
    
    
    app.run(debug=True)