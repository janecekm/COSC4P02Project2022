import json
from selenium import webdriver
from selenium.webdriver.common.by import By
#driver = webdriver.Chrome()
driver = webdriver.Firefox()
driver.get("https://cg2022.gems.pro/Result/Calendar.aspx?SetLanguage=en-CA&Grouping=S")
driver.title

MainInfo = {}

temp = driver.find_element(By.ID,"ctl00_ctl00_divDataContainer")
print(temp)
mainTable = temp.find_elements(By.TAG_NAME,"table")[1]

rows = mainTable.find_elements(By.TAG_NAME,"tbody")[1:]

name = ""
tem = []
for row in rows:
    if row.get_attribute("id").startswith("ctl00"):#not titles
        details = row.find_elements(By.TAG_NAME,"tr")
        
        for detail in details:
            t = {}
            det = detail.find_elements(By.TAG_NAME,"td")
            print(det[5].text)
            t["date"] = det[3].text
            t["time"] = det[4].text
            t["specific-event"] = det[5].text
            t["stage"] = det[6].text
            t["location"] = det[7].text
            tem.append(t)
    else:
        MainInfo[name] = tem
        tem = []
        name = row.text
        print(row.text)
print(MainInfo)

driver.close()
