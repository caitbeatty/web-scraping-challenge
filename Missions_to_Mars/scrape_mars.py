from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time
import pymongo
from selenium import webdriver




def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ##first question
#URL to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'
# Retrieve page with the requests module
    browser.visit(nasa_url)
    html = browser.html
    time.sleep(5)
    soup = BeautifulSoup(html, 'html.parser')
    #get all stories
    news_feed = soup.find_all('li', class_='slide')
    #print(news_feed[0])
    first = news_feed[0]
    #first
    news_title = first.find('div', class_='content_title').text
    news_p = first.find('div', class_='article_teaser_body').text
#next question on image
    #image URL to be scraped
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)
    html = browser.html

    time.sleep(3)
    soup = BeautifulSoup(html, 'html.parser')
    relative_image_path = soup.find_all('img', class_= 'headerimage fade-in')[0]["src"]
    #relative_image_path
    base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    featured_image_url = base_url + relative_image_path
    #featured_image_url

    ##question 3
    #table part of hw
    #URL to be scraped
    facts_url = 'https://space-facts.com/mars/'
    #scrape into a table
    tables = pd.read_html(facts_url)
    #tables
    df = tables[0]
    df.columns = ['Description','Mars']
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    df.to_html('clean_table.html')

    ## question 4
    #mars hemispheres to get hemisphere_image_urls 
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    html = browser.html

    time.sleep(2)
    soup = BeautifulSoup(html, 'html.parser')
    #need to get all images 
    group_list = soup.find_all(class_= 'description')
    #get titles 
    title_list = []
    for name in group_list:
        title_list.append(name.a.h3.text)
    #title_list

    browser.visit(hemi_url)
    hemisphere_image_urls=[]
    for x in range(len(title_list)):
        browser.click_link_by_partial_text(title_list[x])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = title_list[x]
        img_url = soup.find(class_='downloads')
        
     #put in dictionary
        hemisphere_dict = {}
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = img_url.a['href']
        hemisphere_image_urls.append(hemisphere_dict)
        browser.back()
    hemisphere_image_urls

    # Close browser
    browser.quit()

    #final dictionary
    mars_dict = {
    "news_title":news_title,
    "news_p":news_p,
    "featured_image_url":featured_image_url,
    "mars_table":html_table,
    "mars_hemispheres":hemisphere_image_urls}

    print (mars_dict)

    #return
    return mars_dict


