import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

'''
Returns the specified course data in JSON format.

USAGE: python3 scrapeCourseInfo.py [courseName] [session] [type]
RECOMMENDED USAGE (if you do this, you'll get an output file!): python3 scrapeCourseInfo.py [courseName] [session] [type] >[>] [whateveryouwantyoufiletobe.whatever]
>> appends, > overwrites
'''
#add session and type options in a formatted url
def scrapeCourseInfo(courseName, session, type):

	#valid sessions: FW, SP,SU
	#valid types: UG, GR, IS, PS, AD
	driver = webdriver.Firefox()
	driver.get("https://brocku.ca/guides-and-timetables/timetables/?session=" + session + "&type=" + type + "&level=All&program="+courseName)

	#this code assumes that courseName is valid. Refer to the google doc for valid codes.
	entries = driver.find_elements(By.XPATH,'//tr[contains(@class,"course-row")]')

	#the attributes of each of the entries are enough to fill out our database.
	#the next step is harvesting these attributes and formatting them nicely for you guys :3

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

	for course in entries:
		dict = {}
		dict["course-code"] = course.get_attribute("data-cc")
		dict["format"] = course.get_attribute("data-class_type")
		dict["duration"] = course.get_attribute("data-duration")
		dict["section"] = course.get_attribute("data-course_section")
		dict["times"] = course.get_attribute("data-class_time")
		dict["days"] = course.get_attribute("data-days")
		dict["location"] = course.get_attribute("data-location")
		dict["room1"] = course.get_attribute("data-room1")
		dict["room2"] = course.get_attribute("data-room2")
		dict["instructor"] = course.get_attribute("data-instructor")

		#we could modify this code to print to file. Or, you could just use a bash redirect....0_0
		print(json.dumps(dict))


def main():

	if (len(sys.argv) < 4):
    print("USAGE: python3 scrapeCourseInfo.py [courseName] [session] [type]")
    return
  
	courseName = sys.argv[1]
	session = sys.argv[2]
	type = sys.argv[3]
	scrapeCourseInfo(courseName,session,type)

main()
