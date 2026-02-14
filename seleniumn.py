import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Setup Browser
chrome_options = Options()
# chrome_options.add_argument("--headless") # Optional: Run without a window
driver = webdriver.Chrome(options=chrome_options)

try:
    print("Opening SauceDemo...")
    driver.get("https://www.saucedemo.com/")

    # 2. Login (This is standard for testing)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # 3. Wait for products to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

    # 4. Fetch Product Data
    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    product_list = []

    for item in items:
        name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
        price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
        product_list.append({"Product": name, "Price": price})

    # 5. Save to Excel
    df = pd.DataFrame(product_list)
    df.to_excel("SauceDemo_Products.xlsx", index=False)
    print("✅ Success! Found", len(df), "products. Data saved to SauceDemo_Products.xlsx")

except Exception as e:
    print(f"❌ An error occurred: {e}")

finally:
    driver.quit()