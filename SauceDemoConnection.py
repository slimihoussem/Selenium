from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.get("http://www.saucedemo.com") 
assert "Swag Labs" in driver.title

elem = driver.find_element(By.ID, "user-name")
elem.clear()
elem.send_keys("standard_user")

elem = driver.find_element(By.ID, "password")
elem.clear()
elem.send_keys("secret_sauc")
time.sleep(5)

elem = driver.find_element(By.ID, "login-button")
elem.send_keys(Keys.RETURN) #elem.click()
time.sleep(10)

assert "Products" in driver.page_source , "login failed"
#driver.save_screenshot("test123.png")
driver.close()
