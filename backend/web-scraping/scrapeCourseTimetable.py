import json
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

'''
Returns the specified course data in JSON format.
NOTE: NEEDS A WRITE TO FILE BLOCK ADDED, OR TO BE USED AS IS WITH TERMINAL REDIRECT TO A FILE
'''
#add session and type options in a formatted url
def scrapeCourseInfo(courseName, session, typ):

	#this inits the driver every time, which I don't love. Attempts at passing
	#it to this function got weird though
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options) #NOTE: Don't use the chrome driver, unless you want to reconfigure it to run headless
	
	#valid sessions: FW, SP,SU
	#valid types: UG, GR, IS, PS, AD
	driver.get("https://brocku.ca/guides-and-timetables/timetables/?session=" + session + "&type=" + typ + "&level=All&program="+courseName)

	#this code assumes that courseName is valid. Refer to the google doc for valid codes.
	entries = driver.find_elements(By.XPATH,'//tr[contains(@class,"course-row")]')

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
		
		return(json.dumps(dict))
	driver.close()
	

def main():


	subjects = ['abed', 'abte', 'actg', 'aded', 'admi', 'adst', 'aesl', 'apco', 'arab', 'astr', 'bchm', 'biol', 'bmed', 'bphy', 'btec', 'btgd', 'cana', 'chem', 'chys', 'clas', 'comm', 'cosc', 'cpcf', 'dart', 'econ', 'edbe', 'educ', 'encw', 'engl', 'ensu', 'entr', 'ersc', 'esci', 'ethc', 'film', 'fnce', 'fren', 'geog', 'germ', 'gree', 'hist', 'hlsc', 'hlsc', 'iasc', 'indg', 'intc', 'ital', 'itis', 'japa', 'kine', 'labr', 'lati', 'ling', 'mand', 'mars', 'math', 'mgmt', 'mktg', 'musi', 'neur', 'nusc', 'obhr', 'oevi', 'oper', 'pcul', 'phil', 'phys', 'pmpb', 'poli', 'port', 'psyc', 'recl', 'russ', 'scie', 'sclc', 'soci', 'span', 'spma', 'stac', 'swah', 'tour', 'visa', 'wgst', 'wrds']

	sessions = ['FW', 'SP', 'SU']
	types = ['UG', 'GR', 'IS', 'PS', 'AD']


	#returns a giant JSON object with sub-objects that are the courses
	dict = {}
	#print("#course-code, format, duration, section, times, days, location, room1, room2, instructor")
	
	for sess in sessions:
		for t in types:
			for course in subjects:
				dict[course + "_" + sess + "_" + t] = scrapeCourseInfo(course,sess,t)
				
	print(json.dumps(dict))

main()
