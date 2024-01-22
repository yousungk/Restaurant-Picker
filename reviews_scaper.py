from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def get_reviews(driver, query):
    driver.get('https://www.google.com/?hl=en')
    driver.find_element(By.NAME, "q").send_keys(query, Keys.ENTER)

    reviews_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Google reviews")
    number_of_reviews = int(reviews_link.text.split()[0].replace(",", ""))
    print(number_of_reviews)
    reviews_link.click()

    all_reviews = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.gws-localreviews__google-review')))
    print(len(all_reviews))

    while len(all_reviews) < number_of_reviews and len(all_reviews) < 50:
        driver.execute_script('arguments[0].scrollIntoView(true);', all_reviews[-1])
        WebDriverWait(driver, 5, 0.25).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class$="activityIndicator"]')))
        all_reviews = driver.find_elements(By.CSS_SELECTOR, 'div.gws-localreviews__google-review')

    reviews = []
    for review in all_reviews:
        try:
            full_text_element = review.find_element(By.CSS_SELECTOR, 'span.review-full-text')
            reviews.append(full_text_element.get_attribute('textContent'))
        except NoSuchElementException:
            pass

    return reviews




