from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

# Setup Chrome and Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Navigate to the first page of reviews for a specific product
    driver.get('https://www.amazon.com/product-reviews/B06W55K9N6')

    all_reviews = []
    max_pages = 2  # Set the maximum number of pages to scrape

    for page in range(max_pages):
        # Wait for reviews to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-hook='review']")))

        # Extract the review elements
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-hook='review']")

        for review_element in review_elements:
            # Extract the title of each review
            title_element = review_element.find_element(By.CSS_SELECTOR, "a[data-hook='review-title']")
            title = title_element.text.strip()

            # Extract the body of each review
            body_element = review_element.find_element(By.CSS_SELECTOR, "span[data-hook='review-body'] span")
            body = body_element.text.strip()

            # Extract the country and date
            date_element = review_element.find_element(By.CSS_SELECTOR, "span[data-hook='review-date']")
            date_text = date_element.text.strip()
            country = date_text.split(' on ')[0].replace('Reviewed in ', '')
            date = date_text.split(' on ')[1]

            # Extract color from the style information
            color = None
            try:
                style_element = review_element.find_element(By.CSS_SELECTOR, "a.a-size-mini.a-link-normal")
                style_text = style_element.text.strip()
                if 'Color:' in style_text:
                    color = style_text.split('Color: ')[1].split('|')[0].strip()
            except NoSuchElementException:
                color = "Not Specified"

            # Check for verified purchase
            verified_purchase = False
            try:
                verified_element = review_element.find_element(By.CSS_SELECTOR, "span[data-hook='avp-badge']")
                verified_purchase = 'Verified Purchase' in verified_element.text
            except NoSuchElementException:
                pass

            # Number of people who found the review helpful
            helpful_count = 0
            try:
                helpful_element = review_element.find_element(By.CSS_SELECTOR, "span[data-hook='helpful-vote-statement']")
                helpful_count_text = helpful_element.text.strip()
                if 'people' in helpful_count_text:
                    helpful_count = int(helpful_count_text.split()[0])
                elif 'One person' in helpful_count_text:
                    helpful_count = 1
            except NoSuchElementException:
                helpful_count = 0  # If no helpful count is found or the element is not present

            # Check for images or videos
            media_elements = review_element.find_elements(By.CSS_SELECTOR, "img.review-image-tile, div.review-video-thumbnail")
            media_count = len(media_elements)

            # Extract the rating
            rating = None  # Initialize rating with None
            rating_elements = review_element.find_elements(By.CSS_SELECTOR, "i.a-icon-star")
            for element in rating_elements:
                class_attribute = element.get_attribute("class")
                if 'a-star-' in class_attribute:
                    rating = class_attribute.split('a-star-')[-1].split(' ')[0]
                    break  # Found the rating, exit the loop

            # Compile all the extracted data into a dictionary
            review_data = {
                'title': title,
                'body': body,
                'date': date,
                'country': country,
                'color': color,
                'verified_purchase': verified_purchase,
                'helpful_count': helpful_count,
                'media_count': media_count,
                'rating': rating + " out of 5 stars" if rating else 'No rating found'
            }
            all_reviews.append(review_data)

        # Wait before checking for the next page to avoid rapid-fire requests
        time.sleep(2)

        # Check if there is a next page and move to it if we're not on the last page of the loop
        if page < max_pages - 1:
            next_button_elements = driver.find_elements(By.CSS_SELECTOR, "li.a-last a")
            if next_button_elements:
                next_button = next_button_elements[0]
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(2)  # Increase wait time to mimic human reading time
            else:
                print("No more pages found.")
                break  # No more pages of reviews to scrape

finally:
    driver.quit()
