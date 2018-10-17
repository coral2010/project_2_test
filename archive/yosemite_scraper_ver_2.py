# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import time
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/yosemite_db')

def scrape():
    print('INITIALIZING DATA SCRAPE FOR YOSEMITE NATIONAL PARK')
    print('-------------------------------------------------------')

    # initialize browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    # use executable path below for mac
    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    # dictionary to hold final scraped data
    yosemite_data = {}

    print('COMMENCING DATA SCRAPE FOR ECONOMIC BENEFITS INFO')
    
    # URL of yosemite articles page to be scraped
    url = 'https://www.nps.gov/yose/learn/news/newsreleases.htm'
    browser.visit(url)
    time.sleep(2)
    # empty lists to hold raw scraped data
    article_links = []
    headlines = []
    article_contents = []
    # empty lists that will hold cleaned scraped data
    years = []
    amounts = []
    job_counts = []
    visitor_counts = []
    # empty list to hold final scraped data
    economic_benefits = []

    # go through pages 1-33 and find links of targeted articles
    for x in range(1, 34):  
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        article_snippets = soup.find_all('li', class_='ListingList-item')
        substring = 'Economic Benefit'
        for article_snippet in article_snippets:
            snippet_headline = article_snippet.find('h3', class_='ListingResults-title').text
            if substring in snippet_headline:
                end_link = article_snippet.find('a')['href']
                article_link = 'https://www.nps.gov' + end_link
                article_links.append(article_link)
        browser.click_link_by_text('Next ')
        time.sleep(1)

    # visit each article link and extract content
    for article_link in article_links:
        browser.visit(article_link)
        article_html = browser.html
        article_soup = BeautifulSoup(article_html, 'html.parser')
        headline = article_soup.find('div', class_='ContentHeader').text
        headline = headline.replace('\n', '')
        headlines.append(headline)
        article_content = article_soup.find('div', class_='ArticleTextGroup').text
        article_contents.append(article_content)
    # loop through headlines and extract economic benefit $ amount (in millions)
    for headline in headlines:
        headline_split = headline.split('$')[1]
        amount = headline_split[:3]
        amounts.append(amount)
    # loop through article contents and extract year, job count, and visitor count
    for article_content in article_contents:
        year_split = article_content.split('Park in ')[1]
        year = year_split[:4]
        years.append(year)
        job_split = article_content.split('supported ')[1]
        job_count = job_split[:5]
        if ',' in job_count:
            job_count = job_count.replace(',', '')
            job_counts.append(job_count)
        elif ' ' in job_count:
            job_count = job_count.replace(' ', '')
            job_counts.append(job_count)
        else: 
            job_counts.append(job_count)
        visitor_split = article_content.split('shows that')[1]
        visitor_count = visitor_split[:10]
        visitor_count = visitor_count.replace(',', '').replace('\xa0', '').replace(' ', '')
        visitor_counts.append(visitor_count)

    # append extract information into economic_benefits dictionary
    economic_benefits.append({'years': years,
                        'amounts': amounts,
                       'job_counts': job_counts,
                       'visitor_counts': visitor_counts})
    # append missing 2015 data
    economic_benefits[0]['years'].insert(2, '2015')
    economic_benefits[0]['amounts'].insert(2, '594')
    economic_benefits[0]['job_counts'].insert(2, '6890')
    economic_benefits[0]['visitor_counts'].insert(2, '4150217')

    
    print('OBTAINED ECONOMIC BENEFITS')
    print('-------------------------------------------------------')

    print('SCRAPING COMPLETED')
    print('-------------------------------------------------------')

    return economic_benefits

if __name__ == '__main__': 
    economic_benefits_data = scrape()
    economic_benefits_collection = client.yosemite_db.economic_benefits
    economic_benefits_collection.update({}, economic_benefits_data[0], upsert=True)
