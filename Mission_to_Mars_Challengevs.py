# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Path to chromedriver
get_ipython().system('which chromedriver')

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# ### Mars Facts

df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()

df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df

df.to_html()

# ### Mars Weather

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Set the a variable called 'html' and run a parser against the variable
html = browser.html
hemi_image_soup = soup(html, 'html.parser')

base_url ="https://astrogeology.usgs.gov"

# Find all of the 'div' elements that have 'item' as a class
hemi_images = hemi_image_soup.find_all("div", class_='item')

for i in hemi_images:
    # Create a dictionary for responses
    hemisphere_dict = {}
    
    # Find the links that get us to the hemisphere page
    href = i.find('a', class_='itemLink product-item')    
    link = base_url + href['href']
    browser.visit(link)
    
    # Repeate the original step to access the html of the new website
    hemi_site_html = browser.html
    hemi_site_soup = soup(hemi_site_html, 'html.parser')
    
    # Identify the title of the image by searching out the h2 title and removing the text
    img_title = hemi_site_soup.find('div', class_='content').find('h2', class_='title').text
    
    #Assign the 'image_title' variable to the 'title' key in the 'hemisphere' dictionary
    hemisphere_dict['title'] = img_title
    
    # Identify the url of the image by searching out the downloads class and removing the href
    img_url = hemi_site_soup.find('div', class_='downloads').find('a')['href']

    #Assign the 'image_url' variable to the 'url_img' key in the 'hemisphere' dictionary
    hemisphere_dict['url_img'] = img_url
    
    # Append dictionary to list
    hemisphere_image_urls.append(hemisphere_dict)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()