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
    mars_data = {}
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    title_div = soup.find('li', class_='slide').find('div', class_='content_title')
    news_title = title_div.text.strip()

    text_div = soup.find('li', class_='slide').find('div', class_='article_teaser_body')
    news_p = text_div.text.strip()

    mars_data['news'] = {'title': news_title, 'detail': news_p}

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    browser.links.find_by_partial_href('spaceimages/images').click()

    html = browser.html
    soup = bs(html, 'html.parser')
    #base_url = 'https://www.jpl.nasa.gov'

    #featured_image = soup.find('div', class_='carousel_items')
    #featured_image_url = base_url + featured_image.article.div.footer.a['data-fancybox-href']
    featured_image_url = soup.body.img['src']
    mars_data['featured_url'] = featured_image_url

    url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(url)
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ['Parameter','Value']
    mars_facts_html = mars_facts_df.to_html()
    mars_facts_html.replace('\n', '')

    mars_data['mars_facts'] = mars_facts_html

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    img_results = soup.find_all('div', class_='item')
    base_url = 'https://astrogeology.usgs.gov'
    url_list = []
    for result in img_results:
        page_url = result.find('a')['href']
        url_list.append(page_url)

    hem_url_list = [base_url + url for url in url_list]
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
    
    mars_data['hemisphere_data'] = hemisphere_image_urls

    browser.quit()

    return mars_data