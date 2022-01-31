import json
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get("https://brocku.ca/guides-and-timetables/glossary/#subject-codes")
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
##        driver.get("https://brocku.ca/webcal/2021/undergrad/"+temp[0].text.lower()+".html")
    else:
        flag = True
##for x in tempy:
#print(programCode)
for code in programCode:
    driver.get("https://brocku.ca/webcal/2021/undergrad/"+code+".html")
    if driver.find_element(By.CLASS_NAME,"pgtitle").text =="Not Found":#this is to see if teh page exist
        pass
    else:
        CourseInfo = []
        for x in driver.find_elements(By.TAG_NAME,"p"):
            if x.get_attribute("class").startswith("cal"):#gets the one related to cal
                CourseInfo.append(x)
        no = 0
        flag = False
        flagNumber = 2
        name = ""
        temp = {}
        tempcounter = 0
        for course in CourseInfo:#gets prerequisty
            
            if flag:
                no = no + 1
            if no == flagNumber:
                #print(course.text)#description
                temp["desc"] = course.text
                no = 0
                flag = False
            if course.get_attribute("class") == "calnormal":
                if course.text.startswith("Prerequisite"):
                    temp["prereq"] = course.text
                 #   print(course.text)#pre req
            if course.get_attribute("class") == "calccode":
                #print(course.text)#course code
                if tempcounter>0:
                    MainInfo[name] = temp
                    print(temp)
                else:
                    tempcounter = tempcounter+1
                if course.text.startswith("*") or course.text.startswith("#"):
                    flagNumber = 3
                    name = course.text[1:]   
                else:
                    flagNumber = 2
                    name = course.text
                
                temp = {}
                flag = True
print(MainInfo)
driver.close()
