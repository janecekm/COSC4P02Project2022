import json
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
'''
Returns the specified course data in JSON format.

USAGE: python3 scrapeCourseInfo.py [courseName] [session] [type]
RECOMMENDED USAGE (if you do this, you'll get an output file!): python3 scrapeCourseInfo.py [courseName] [session] [type] >[>] [whateveryouwantyoufiletobe.whatever]
>> appends, > overwrites
'''
#add session and type options in a formatted url
def scrapeCourseInfo(courseName, session, typ, driver):


	
	#valid sessions: FW, SP,SU
	#valid types: UG, GR, IS, PS, AD
	driver.get("https://brocku.ca/guides-and-timetables/timetables/?session=" + session + "&type=" + typ + "&level=All&program="+courseName)
	sleep(3)
	#this code assumes that courseName is valid. Refer to the google doc for valid codes.
	entries = driver.find_elements(By.XPATH,'//tr[contains(@class,"course-row")]')
	# print(courseName)
	'''
	Code
	Format
	Duration
	Section
	Times
	Instructor
	Location

	<tr id="4332101" class="course-row special faculty-SC" data-cid="4332101" data-cc="COSC0N01" data-year="2021" data-session="FW" data-type="UG" data-subtype="UG" data-level="All" data-fn2_notes="OE" data-duration="2" data-class_type="PRO" data-course_section="1" data-days="       " data-class_time="Project Course" data-room1="TBS" data-room2="" data-location="TBS" data-location_desc="" data-instructor="See dept." data-msg="0" data-main_flag="1" data-secondary_type="E" data-startdate="1631073600" data-enddate="1638853200" data-faculty_code="SC" data-faculty_desc="Mathematics and Science">

	'''

	#course-code, format, duration, section, times, days, location, room1, room2, instructor
	outer = {}
	for course in entries:
		dict = {}
		dict["cc"] = course.get_attribute("data-cc").replace(',','')
		dict["type"] = course.get_attribute("data-class_type").replace(',','')
		dict["duration"] = course.get_attribute("data-duration").replace(',','')
		dict["sec"] = course.get_attribute("data-course_section").replace(',','')
		dict["time"] = course.get_attribute("data-class_time").replace(',','')
		dict["days"] = course.get_attribute("data-days").replace(',','')
		dict["loc"] = course.get_attribute("data-location").replace(',','')
		dict["room1"] = course.get_attribute("data-room1").replace(',','')
		dict["room2"] = course.get_attribute("data-room2").replace(',','')
		dict["instructor"] = course.get_attribute("data-instructor").replace(',','')
		
		title = course.find_element(By.CLASS_NAME,"title")
		dict["title"] = title.text

		print(json.dumps(dict))
	

def main():

	sessions = ['FW', 'SP', 'SU']
	types = ['UG', 'GR', 'IS', 'PS', 'AD']

	

	
	#Returns seperate json objects for each offering
	#print("#course-code, format, duration, section, times, days, location, room1, room2, instructor")
	for sess in sessions:
		for t in types:
			driver.get("https://brocku.ca/guides-and-timetables/timetables/?session="+sess+"&type="+t+"&level=all")
			sleep(3)
			subjects = []
			programs = driver.find_element(By.CLASS_NAME,"programs")
			courses = programs.find_elements(By.TAG_NAME,"li")
			for c in courses:
				tag = c.find_element(By.TAG_NAME,"a")
				subjects.append(tag.get_attribute("data-program"))
			# print(subjects)
			for course in subjects:
				scrapeCourseInfo(course,sess,t,driver)
			
	
	driver.close()
main()