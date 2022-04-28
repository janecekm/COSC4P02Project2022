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
firstpass = True
for row in rows:
    if row.get_attribute("id").startswith("ctl00"):#not titles
        details = row.find_elements(By.TAG_NAME,"tr")
        
        for detail in details:
            t = {}
            det = detail.find_elements(By.TAG_NAME,"td")
            # print(det[5].text)
            t["sports"] = name
            tempdate = [x.strip() for x in det[3].text.split(",")]
            t["month"],t["date"] = tempdate[1].split(" ")
            t["day"] = tempdate[0]
            t["year"] = tempdate[2]
            # t["date"] = det[3].text
            t["time"] = det[4].text
            # t["specific-event"] = det[5].text
            tempevent = det[5].text.split(" ")
            if len(tempevent) == 1:#only gender
                t["gender"] = tempevent[0]
                t["specific-event"] = name
            else:
                t["gender"] = tempevent[len(tempevent)-1]
                t["specific-event"] = " ".join(tempevent[:len(tempevent)-1])
            # t["stage"] = det[6].text
            tempstage = [x.strip() for x in det[6].text.split("|")]
            tempstage = "-".join(tempstage)
            tempstage = [x.strip() for x in tempstage.split("-")]
            t["stage"] = tempstage[0]
            t["game"] = " ".join(tempstage[1:])
            # t["game"] = " ".join(tempevent[1:])
            t["venue"] = det[7].text
            print(json.dumps(t))
    else:
            name = row.text
print(MainInfo)

driver.close()
