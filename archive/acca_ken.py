# URL of page to be scraped
url = 'https://www.hikespeak.com/sierras/yosemite/'
browser.visit(url) 

# Examine the results, then determine element that contains sought info
# results are returned as an iterable list

results = soup.find_all("tr")


## Probably need a loop here for all 20 rows

# Loop through returned results
for result in results:
    # Error handling
    try:
        # Identify and return title of listing
        trail = result.find("td", class_="column-2").text
        distance = result.find("td", class_="column-3").text
        coordinates = result.find("td", class_="column-4").text
        

        # Run only if title, price, and link are available
        if (trail and distance and coordinates):
            # Print results
            print('-------------')
            print(trail)
            print(distance)
            print(coordinates)
            

            # Dictionary to be inserted as a MongoDB document
            post = {
                'trail': trail,
                'distance': distance,
                'coordinates': coordinates
             }

            collection.insert_one(post)

    except Exception as e:
        print(e)