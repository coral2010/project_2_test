# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo

 # Initialize PyMongo to work with MongoDBs
trail_table_conn = 'mongodb://localhost:27017'
trail_table_client = pymongo.MongoClient(trail_table_conn)

 # Define database and collection
trail_table_db = trail_table_client.trail_table_db
trail_table_collection = trail_table_db.items

# URL of page to be scraped
trail_table_url = 'https://www.yosemitehikes.com/hikes.htm'

# Retrieve page with the requests module
response = requests.get(trail_table_url)
# Create BeautifulSoup object; parse with 'lxml'
soup = BeautifulSoup(response.text, 'lxml')

# Examine the results, then determine element that contains sought info
# results are returned as an iterable list
trail_table_results = soup.find_all('tr')

# Loop through returned results
for trail_table_result in trail_table_results:
    # Error handling
    try:
        # Identify and return trail name
        trail_name = trail_table_result.find('td', column='Trail').text
        # Identify and return trail's distance
        try:
            raw_distance = trail_table_result.find('td', column="Distance (miles/km)").text
            #remove string after " (" to get only distance in miles
            distance = raw_distance[:raw_distance.find(" (")]
        except Exception as distance:
            distance = trail_table_result.find('td', column="Distance (miles/km)").text
        # Identify and return trail's elevation
        try:
            raw_elevation = trail_table_result.find('td', column="Elevation Gain (feet/meters)").text
            #remove string after " (" to get only elevation in feet
            elevation = raw_elevation[:raw_elevation.find(" (")]
        except Exception as elevation:
            elevation = trail_table_result.find('td', column="Elevation Gain (feet/meters)").text
        # Identify and return trail's crowd rating
        crowd = str(trail_table_result.find('td', column="Crowd Factor"))[44]
        # Identify and return trail's scenery rating
        scenery = str(trail_table_result.find('td', column="Scenery Factor"))[-14]
        # Identify and return trail's difficulty rating
        difficulty = str(trail_table_result.find('td', column="Difficulty"))[-14]


        #Dictionary to be inserted as a MongoDB document
        trail_table_post = {
            'trail_name': trail_name,
            'distance': distance,
            'elevation': elevation,
            'crowd': crowd,
            'scenery': scenery,
            'difficulty': difficulty
        }

        trail_table_collection.insert_one(trail_table_post)

    except Exception as e:
        print(e)
        
trail_table_listings = trail_table_db.items.find()