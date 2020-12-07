from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import pymongo

def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # This module will scrape the mars data, using splinter and beautifulsoup
    mars_data = {}
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    # Waiting 2 Sec for page to load as it was throwing Nonetype error in execution
    time.sleep(2)

    # Getting Title of the latest news
    title_div = soup.find('li', class_='slide').find('div', class_='content_title')
    news_title = title_div.text.strip()
    # Getting Description of the Latest News
    text_div = soup.find('li', class_='slide').find('div', class_='article_teaser_body')
    news_p = text_div.text.strip()

    # Loading Title and Description to Dictionary
    mars_data['news'] = {'title': news_title, 'detail': news_p}

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Navigating through NASA Mars site to get Full Featured Image
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    browser.links.find_by_partial_href('spaceimages/images').click()

    html = browser.html
    soup = bs(html, 'html.parser')
    
    # Fetching Feature Image URL and storing in Dictionary
    featured_image_url = soup.body.img['src']
    mars_data['featured_url'] = featured_image_url

    # Getting Mars Facts Data table
    url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(url)
    mars_facts_df = mars_facts[0]
    # Renaming columns and updating index column
    mars_facts_df.columns = ['Description','Mars']
    mars_facts_df.set_index('Description', inplace = True)
    mars_facts_html = mars_facts_df.to_html()
    mars_facts_html.replace('\n', '')

    # Storing Mars Facts table in Dictionary
    mars_data['mars_facts'] = mars_facts_html

    # Following section will get Mars Hemisphere Details
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    img_results = soup.find_all('div', class_='item')
    base_url = 'https://astrogeology.usgs.gov'
    url_list = []
    # Storing details page URL for Mars Hemisphere
    for result in img_results:
        page_url = result.find('a')['href']
        url_list.append(page_url)

    hem_url_list = [base_url + url for url in url_list]
    # Browsing through Mars Hemisphere pages and storing Title and High Resolution Image link
    hemisphere_image_urls = []
    for url in hem_url_list:
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        title_h2 = soup.find('h2', class_='title')
        title = title_h2.text.strip()
        
        img_div = soup.find('img', class_='wide-image')
        img_url = base_url + img_div['src']

        img_dict = {'title':title, 'img_url':img_url}
        hemisphere_image_urls.append(img_dict)
    
    # Storing Hemisphere informtion in Dictionary
    mars_data['hemisphere_data'] = hemisphere_image_urls

    browser.quit()

    # Returning Mars Data Dictionary to the caller
    return mars_data