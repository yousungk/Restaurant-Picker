from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time

# inputs
cuisine = "italian"
town = "FORT LEE"
state = "NJ"
keywords = "romantic" # used to search in review
price = "$$" # $, $$, $$$, $$$$

# scrape google maps data
# get number of reviews, reviews, rating, contains keywords, get price range, location
# get address, google map link, name

# set up web driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.google.com/maps")

# type into google maps
searchBox = driver.find_element(by=By.ID, value="searchboxinput")
searchBox.send_keys(f"{cuisine} near {town}, {state}", Keys.ENTER)

# filter for price range
time.sleep(3)
priceMap = {"$": "Inexpensive", "$$": "Moderate", "$$$": "Expensive", "$$$$":"Very Expensive"}

priceButton = driver.find_element(by=By.CSS_SELECTOR, value="[aria-label='Price']")
if priceButton:
    priceButton.click()

priceChoice = driver.find_element(by=By.CSS_SELECTOR, value=f"[aria-label={priceMap[price]}")
priceChoice.click()

doneButton = driver.find_element(by=By.CSS_SELECTOR, value="[jsaction='actionmenu.done; keydown:actionmenu.done']")
doneButton.click()

# get restaurant list
def scroll_for_duration(driver, seconds):
    divSideBar = driver.find_element(by=By.CSS_SELECTOR, value=f"[aria-label='Results for {cuisine} near {town}, {state}']")

    end_time = time.time() + seconds
    while time.time() < end_time:
        # Scroll down using the keyboard arrow down key
        divSideBar.send_keys(Keys.PAGE_DOWN)

scroll_for_duration(driver, 10)

restaurantList = []
restaurants = driver.find_elements(by=By.CLASS_NAME, value="TFQHme")
for restaurant in restaurants:
    # Get the next sibling div
    next_sibling_div = restaurant.find_element(By.XPATH, "following-sibling::div")
    restaurantList.append(next_sibling_div.get_attribute("innerHTML"))

print(restaurantList)
print(len(restaurantList))

# get number of reviews, reviews, rating, contains keywords, get price range, location
# get address, google map link, name

# get instagram hashtag post data
# get number of instagram posts for the restaurant

# get number of news mentions


