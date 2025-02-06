from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

# Amazon URL
url = "https://www.amazon.eg/-/en/s?i=videogames&srs=26082362031&rh=n%3A26082362031&s=popularity-rank&fs=true&language=en&qid=1738805526&xpid=nLKhzoibWfEx5&ref=sr_pg_1"

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(service=Service(), options=options)

driver.get(url)
wait = WebDriverWait(driver, 10)  # Explicit wait for up to 10 seconds


Product_Names = []
Product_Prices = []
csv_file_path = 'products.csv'
while True:
    # Extract and print prices
    Product_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//h2[@class='a-size-medium a-spacing-none a-color-base a-text-normal']")))
    prices_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-price-whole']")))
    
    # Extract the product names and prices and add to lists
    for Product_Name, price_element in zip(Product_list, prices_list):
        Product_Names.append(Product_Name.text)
        Product_Prices.append(price_element.text)

        # Create a DataFrame for each product and append directly to CSV
        df = pd.DataFrame({"Name": [Product_Name.text], "Price": [price_element.text]})
        df.to_csv(csv_file_path, mode='a', header=not pd.io.common.file_exists(csv_file_path), index=False)

    try:
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@class='s-list-item-margin-right-adjustment']/span[@class='a-list-item']/a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator']"))) 
        next_url = next_button.get_attribute("href")
        print(next_url)
        # Navigate directly to the next page
        driver.get(next_url)
    except Exception as e:
        print("No more pages or error:", e)
        break

driver.quit()