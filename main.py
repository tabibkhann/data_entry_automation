import time
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

WEBSITE_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_LINK = "https://forms.gle/ymzwRQiKUP7As87LA"

# scrape the data from the website
response = requests.get(WEBSITE_URL, headers={
    "Accept-Language":"en-US"
  })
data = response.text
soup = BeautifulSoup(data, "html.parser")

# gets all the links of the listing
links = soup.find_all('a')
destination_url = "https://www.zillow.com/"
filtered_urls = []

for link in links:
    href = link.get('href')
    if href and destination_url in href:
        filtered_urls.append(href)

# print(filtered_urls)

# gets prices of all the listing
prices = soup.find_all('span', class_='PropertyCardWrapper__StyledPriceLine')
filtered_prices = []
for price in prices:
    price_text = price.get_text()
    cleaned_price = re.sub(r'[^\d,$]', '', price_text)
    filtered_prices.append(cleaned_price)

# print(filtered_prices)

# gets address of all the listing
addresses = soup.find_all('address')
filtered_address = []
for address in addresses:
    address_text = address.get_text()
    cleaned_address = re.sub(r'\s*\|\s*', ' ', address_text)
    cleaned_address = re.sub(r'\s+', ' ', cleaned_address)
    cleaned_address = cleaned_address.strip()
    filtered_address.append(cleaned_address)

# print(filtered_address)


# using selenium opens the form url
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_LINK)

# fills all the fields of the form and submits it
for n in range(len(filtered_prices)):
    time.sleep(3)
    property_add = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_add.send_keys(filtered_address[n])

    property_price = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_price.send_keys(filtered_prices[n])

    property_link = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_link.send_keys(filtered_urls[n+1])

    # time.sleep(3)
    submit = driver.find_element(By.CLASS_NAME, value="uArJ5e")
    submit.send_keys(Keys.ENTER)

    time.sleep(3)
    new_response = driver.find_element(By.LINK_TEXT, value="Submit another response")
    new_response.send_keys(Keys.ENTER)

