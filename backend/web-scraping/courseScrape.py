import json
from joblib import PrintTime
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys

sys.stdout.reconfigure(encoding='utf-8')


driver = webdriver.Chrome()

programCode = []
# for row in rows:
#     if flag:
#         temp = row.find_elements(By.TAG_NAME,"td")
#         programCode.append(temp[0].text.lower())
# ##        driver.get("https://brocku.ca/webcal/2021/undergrad/"+temp[0].text.lower()+".html")
#     else:
#         flag = True
##for x in tempy:
driver.get("https://brocku.ca/webcal/2021/undergrad")
rows = driver.find_elements(By.CLASS_NAME,"contenttitle")
#print(programCode)
for row in rows:
    t = row.find_element(By.TAG_NAME,'a')
    s = t.get_attribute("href")
    programCode.append(s)
# for code in programCode:
# driver.get(programCode[0])
# link = "https://brocku.ca"
# code = "cosc"
# driver.get("https://brocku.ca/webcal/2021/undergrad/"+code+".html")
for program in programCode:
    driver.get(program)
    if driver.find_element(By.CLASS_NAME,"pgtitle").text =="Not Found":#this is to see if teh page exist
        pass
    else:
        CourseInfo = []
        for x in driver.find_elements(By.TAG_NAME,"p"):
            if x.get_attribute("class").startswith("cal"):#gets the one related to cal
                CourseInfo.append(x)
        no = 0
        flag = False
        primaryOrSecond = 0 #  1 for main, 2 for secondary
        flagNumber = 2
        name = ""
        # temp = {"courseCode":"","title":"","frmt":"","description":"","prereq":"","xlist":"","restriction":""} this is the format, but if something is missing, just doesn't link it
        temp = {}
        tempcounter = 0
        for course in CourseInfo:#gets prerequisty
            
            if flag:
                no = no + 1
            if no == flagNumber:
                #print(course.text)#description
                temp["description"] = course.text
                no = 0
                flag = False
            if course.get_attribute("class") == "calnormal":
                if course.text.startswith("Prerequisite"):
                    temp["prereq"] = course.text.replace('Prerequisite(s): ', '')
                    #   print(course.text)#pre req
                if course.text.startswith("(also offered as"):
                        temp["xlist"] = course.text.replace("(also offered as ","")
                if course.text.startswith("Restriction: "):
                    temp["restriction"] = course.text.replace("Restriction: ","")
            if course.get_attribute("class") == "calitalic":#this is the format
                temp["frmt"] = course.text
            if course.get_attribute("class")== "calcname":
                temp["title"] = course.text
            if course.get_attribute("class") == "calccode":
                #print(course.text)#course code
                if tempcounter>0:
                    temp["code"] = name
                    print(temp)
                    # MainInfo[name] = temp
                else:
                    tempcounter = tempcounter+1
                if course.text.startswith("*") or course.text.startswith("#"):
                    # mainorsecondaryornone = 1 if course.text.startswith("*") else 2
                    flagNumber = 3
                    name = course.text[1:]   
                else:
                    flagNumber = 2
                    name = course.text
                
                temp = {}
                flag = True

# # with open('courseinfo.txt', 'w+') as f:
# #         f.writelines(json.dumps(MainInfo))
# print(json.dumps(MainInfo))
driver.close()
