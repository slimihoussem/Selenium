from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get("http://google.com")

    element = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID,"lb"))
    )

    print(f"Element found")

finally:
    # Close the browser
    driver.quit()