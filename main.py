from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time
import reviews_scaper

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
def scroll_for_duration(seconds, origin_element):
    end_time = time.time() + seconds
    while time.time() < end_time:
        # Scroll down using the keyboard arrow down key
        origin_element.send_keys(Keys.PAGE_DOWN)


divSideBar = driver.find_element(by=By.CSS_SELECTOR, value=f"[aria-label='Results for {cuisine} near {town}, {state}']")
scroll_for_duration(2, divSideBar)

restaurantList = []
restaurants = driver.find_elements(by=By.CLASS_NAME, value="TFQHme")
restaurants = restaurants[:15] if len(restaurants) > 15 else restaurants
for restaurant in restaurants:
    # Get the next sibling div
    next_sibling_div = restaurant.find_element(By.XPATH, "following-sibling::div")
    anchor = next_sibling_div.find_element(by=By.TAG_NAME, value="a")
    # list of dictionary of (name : dictionary)
    restaurantList.append({anchor.get_attribute("aria-label"): {
        "link": anchor.get_attribute("href")}
    })

# get stats for each restaurant
for restaurant in restaurantList:
    for name, details in restaurant.items():
        driver.get(details["link"])

        # get rating
        rating = driver.find_element(By.CSS_SELECTOR, f"[aria-label*=' stars']").get_attribute("aria-label")
        print(rating)

        # get review count
        reviewCount = driver.find_element(By.CSS_SELECTOR, f"[aria-label*=' reviews']").get_attribute("aria-label")
        print(reviewCount)

        # get price
        price = driver.find_element(By.CSS_SELECTOR, f"[aria-label*='Price: ']").get_attribute("aria-label")
        print(price)

        # get top < 50 reviews for keywords
        reviews = reviews_scaper.get_reviews(driver, f"{name} {town} {state}")
        print(reviews)
        print(len(reviews))

    # get number of reviews, reviews, rating, contains keywords, get price range, location

    # get number of bookings

    # export data in CSV

    # create API

    # create restaurant recommender website

    # create graph to show how the rating and reviews change over time for restaurants
    # for top NYC restaurants
    # use Wayback Machine



