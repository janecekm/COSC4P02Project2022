from asyncio import events
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
# driver = webdriver.Firefox()
driver.get("https://niagara2022games.ca/venues")
driver.title

rows = driver.find_elements(By.TAG_NAME, "article")
for row in rows:
    temp = {}
    temp["location"] = row.find_element(By.TAG_NAME, "h1").text
    temp["town"] = row.find_element(By.TAG_NAME, "h2").text
    temp["description"] = row.find_element(By.TAG_NAME, "p").text
    temp["events"] = []
    events = row.find_elements(By.TAG_NAME,"small")
    for event in events:
        temp["events"].append(event.text)
    print(json.dumps(temp))
driver.close()