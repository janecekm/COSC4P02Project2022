
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
    
# subjects = ['abed', 'abte', 'actg', 'aded', 'admi', 'adst', 'aesl', 'apco', 'arab', 'astr', 'bchm', 'biol', 'bmed', 'bphy', 'btec', 'btgd', 'cana', 'chem', 'chys', 'clas', 'comm', 'cosc', 'cpcf', 'dart', 'econ', 'edbe', 'educ', 'encw', 'engl', 'ensu', 'entr', 'ersc', 'esci', 'ethc', 'film', 'fnce', 'fren', 'geog', 'germ', 'gree', 'hist', 'hlsc', 'iasc', 'indg', 'intc', 'ital', 'itis', 'japa', 'kine', 'labr', 'lati', 'ling', 'mand', 'mars', 'math', 'mgmt', 'mktg', 'musi', 'neur', 'nusc', 'obhr', 'oevi', 'oper', 'pcul', 'phil', 'phys', 'pmpb', 'poli', 'port', 'psyc', 'recl', 'russ', 'scie', 'sclc', 'soci', 'span', 'spma', 'stac', 'swah', 'tour', 'visa', 'wgst', 'wrds']
# 
# 
def run(driver):
    subjects = []

    Days ={"Mon.":"Monday","Tue.":"Tuesday","Wed.":"Wednesday","Thu.":"Thursday","Fri.":"Friday","Sat.":"Saturday","Sun.":"Sunday"}
    types = ['UG', 'GR', 'IS', 'PS', 'AD']
    examYear = ""
    examMonth = ""
    # driver = webdriver.Chrome()

    driver.get("https://brocku.ca/guides-and-timetables/timetables/?session=fw&type=ex&level=all")

    programs = driver.find_element(By.CLASS_NAME,"programs")

    courses = programs.find_elements(By.TAG_NAME,"li")
    #https://brocku.ca/guides-and-timetables/timetables/?session=fw&type=ex&level=all&program=ACTG&academicyear=2021&period=April
    for course in courses:
        tag = course.find_element(By.TAG_NAME,"a")
        subjects.append(tag.get_attribute("data-program")) #gets all the course code
        examYear = tag.get_attribute("data-year")
        examMonth = tag.get_attribute("data-period")
    #Returns seperate json objects for each offering
    #print("#course-code, format, duration, section, times, days, location, room1, room2, instructor")
    for subject in subjects:
        # scrapeCourseInfo(subject,"fw","ex",examYear,examMonth,driver)
        driver.get("https://brocku.ca/guides-and-timetables/timetables/?session=fw&type=ex&level=all&program="+subject+"&academicyear=2021&period=april")
        sleep(10)
        exams = driver.find_elements(By.XPATH,'//tr[contains(@class,"exam-row")]')

        for exam in exams:
            solution = {}
            solution["code"] = exam.get_attribute("data-cc")
            # solution["location"] = exam.get_attribute("data-location")
            solution["time"] = exam.get_attribute("data-start") +"-"+exam.get_attribute("data-end")
            # solution["endTime"] = exam.get_attribute("data-end")
            # solution["Day"] = exam.get_attribute("data-day")
            day = exam.get_attribute("data-day").split()
            solution["day"] = Days[day[0]]
            solution["dayNumber"] = str(day[2])
            solution["month"] = exam.get_attribute("data-period")
            solution["sec"] = exam.get_attribute("data-section")
            if(exam.get_attribute("data-location")!="See notes"):
                solution["location"] = exam.get_attribute("data-location")
            else:
                exam.click()
                sleep(10)#don't know why it works
                lis = exam.find_elements(By.TAG_NAME,"li")
                solution["location"] = lis[len(lis)-1].text
            print(json.dumps(solution))

    # for sess in sessions:
    # 	for t in types:
    # 		for course in subjects:
    # 			scrapeCourseInfo(course,sess,t,driver)
            
    driver.close()