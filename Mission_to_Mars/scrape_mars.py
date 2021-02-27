from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import pymongo
import requests

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
    #driver= webdriver.Chrome()

def scraper():
    browser = init_browser()
    main_dict = {}

    # Begin Scraping everything that was done in the .ipynb
    # Scrape Mars News
    #Set up url to Scrape the NASA Mars News Site
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html=browser.html
    soup=bs(html, "html.parser")
    # Get news_title and news_p
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Set up JPL url and scrape the featured image
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(jpl_url)
    html = browser.html
    jpl_soup = bs(html, "html.parser")
    rel_image_path = jpl_soup.find_all('img')[1]['src']
    if jpl_url.endswith('index.html'):
        jpl_url = jpl_url[:-10]
    featured_image_path = jpl_url + rel_image_path

    # Scrape mars facts into an html table
    facts_url = "https://space-facts.com/mars/"
    facts_table = pd.read_html(facts_url)
    facts_df = facts_table[2]
    facts_df.columns = ["Profile", "Value"]
    facts_table_html = facts_df.to_html()
    facts_table_html.replace('\n','')

    # Scrape Hemisphere images and names
    hems_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hems_url)
    hems_html = browser.html
    hems_soup = bs(hems_html, "html.parser")
    hems = hems_soup.find('div', class_='collapsible results')
    mars_hems = hems.find_all('div', class_='item')
    hemisphere_image_urls = []
    # Use the for loop to collect data from each hemisphere url
    for x in mars_hems:
        # Title
        hem = x.find('div', class_='description')
        title = hem.h3.text
        # Image links
        hems_link = hem.a['href']
        browser.visit('https://astrogeology.usgs.gov/' + hems_link)
        html=browser.html
        img_soup=bs(html, 'html.parser')
        img_src = img_soup.find('li').a['href']

        # Store info in a dict
        hems_dict={'title': title,'image_url': img_src}
        hemisphere_image_urls.append(hems_dict)
    
    # put all data into the main_dict to prepare for the flask app
    main_dict = {
        "News Title": news_title,
        "News Paragraph": news_p,
        "Featured Image URL": featured_image_path,
        "Fact Table": str(facts_table_html),
        "Hemisphere Images": hemisphere_image_urls
    }

    # Return the dictionary
    return main_dict
