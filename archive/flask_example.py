from flask import Flask, render_template
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
    yosemite_data = client.yosemite_db.scraped_data.find_one()
    return render_template('index.html', scraped_data=scraped_data)

@app.route("/data")
def data():

    data = yosemite_scraper.scrape()
    scraped_data = client.yosemite_db.scraped_data
    scraped_data.update({}, data, upsert=True)

    results = list(client.yosemite_db.scraped_data.find())
    for result in results:
        del(result['_id'])
    return json.dumps(results)
    
if __name__ == '__main__':    
    
    
    app.run(debug=True)