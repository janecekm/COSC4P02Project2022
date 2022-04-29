from selenium import webdriver
from selenium.webdriver.common.by import By
import json
def run(driver):
    # driver = webdriver.Chrome()
    driver.get("https://brocku.ca/programs")
    content = driver.find_element(By.ID,"content")
    items = content.find_elements(By.CLASS_NAME,"item")
    for item in items:
        programs = {}
        a = item.find_element(By.TAG_NAME,"a")
        programs[a.text] = a.get_attribute("href")
        print(json.dumps(programs))

    driver.close()