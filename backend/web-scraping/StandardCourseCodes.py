from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get("https://brocku.ca/guides-and-timetables/glossary/#subject-codes%22")
driver.title

tableOfresources = driver.find_elements(By.CLASS_NAME,"vc-table-plugin-theme-classic")

rows = tableOfresources[1].find_elements(By.TAG_NAME,"tr")
MainInfo={}

flag= False
programCode = []
for row in rows:
    if flag:
        temp = row.find_elements(By.TAG_NAME,"td")
        programCode.append(temp[0].text.lower())
##        driver.get("https://brocku.ca/webcal/2021/undergrad/%22+temp[0].text.lower()+%22.html%22)
    else:
        flag = True
driver.close()
print(programCode)
# with open('StandardCourseCodes.txt', 'a') as f:
#     for code in programCode:
#         f.write(code)