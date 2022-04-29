import json
from selenium import webdriver
from selenium.webdriver.common.by import By
def run(driver):
    driver.get("https://brocku.ca/academic-advising/find-your-advisor/")
    driver.title
    MainContent = []
    maincontent = driver.find_element(By.ID, "page-content")
    rows = maincontent.find_elements(By.TAG_NAME,"tr")
    for row in rows:
        values = row.find_elements(By.TAG_NAME,"td")
        temp = []
        if values[0].text == "Department" or values[0].text == "Advisor":
            continue
        for value in values:
            temp.append(value.text)
        MainContent.append(temp)
    print(MainContent)
    driver.close()
    
