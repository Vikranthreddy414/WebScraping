from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome and Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.get('https://www.amazon.com/dp/B08YS47HJZ/ref=sspa_dk_browse_1/?asc_source=01HFY6QA7FYP0YEFD1ZY3XMFP8&tag=snx78-20')
    # Wait for the title to load and find it
    product_title_element = driver.find_element(By.ID, 'productTitle')
    #price = driver.find_element(By.ID, 'priceblock_ourprice').text.strip()
    # Wait for the price elements to load and find them
    price_symbol = driver.find_element(By.CLASS_NAME, 'a-price-symbol').text
    price_whole = driver.find_element(By.CLASS_NAME, 'a-price-whole').text.rstrip('.')
    price_fraction = driver.find_element(By.CLASS_NAME, 'a-price-fraction').text

    # Combine the parts to get the full price, ensuring the decimal point is included
    full_price = f"{price_symbol}{price_whole}.{price_fraction}"
    
    # Extracting the number of reviews
    num_reviews = driver.find_element(By.ID, 'acrCustomerReviewText').text.strip()

    # Rest of your scraping code to get price, etc...
    print(product_title_element.text.strip())
    print(f"Price: {full_price}")
    print(f"Number of reviews: {num_reviews}")
    
    # Wait for the "About this item" section to load and find it
    about_this_item_section = driver.find_element(By.ID, 'feature-bullets')

    # Find all list items within the unordered list
    bullet_points = about_this_item_section.find_elements(By.TAG_NAME, 'li')

    # Extract the text of each bullet point
    about_this_item_details = [bullet_point.text for bullet_point in bullet_points if bullet_point.text]

    
    
    #-------------------------------
    
    # Assuming the table has an ID or a unique class, find the table
    product_overview_table = driver.find_element(By.ID, 'productOverview_feature_div')
    
    # Locate all the rows in the table
    rows = product_overview_table.find_elements(By.TAG_NAME, 'tr')
    
    # Dictionary to hold the product overview information
    product_overview = {}
    
    # Iterate over the rows and extract the information
    for row in rows:
        # Each detail is in a separate cell. Here we assume that the first cell contains
        # the name of the detail (e.g., "Brand") and the second cell contains the value.
        cells = row.find_elements(By.TAG_NAME, 'td')
        
        # Check if there are two cells as expected
        if len(cells) == 2:
            detail_name = cells[0].text.strip()
            detail_value = cells[1].text.strip()
            
            # Add the details to the dictionary
            product_overview[detail_name] = detail_value

    # Print the product overview details
    for detail_name, detail_value in product_overview.items():
        print(f"{detail_name}: {detail_value}")
        
    #------------------------------
    
    # Print the "About this item" details
    print("About this item:")
    for detail in about_this_item_details:
        print(f"- {detail}")
    
    
finally:
    driver.quit()