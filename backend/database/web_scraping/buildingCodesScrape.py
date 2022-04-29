#Gets the building codes
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

def run(driver):
	# if you're running the Chrome driver, change this line!
	driver.get("https://brocku.ca/directory/building-codes/")

	# format CODE, BUILDING
	codeElements = driver.find_elements(By.CLASS_NAME,'code')
	descElements = driver.find_elements(By.CLASS_NAME,'description')

	#combine the code and descElements into a dict
	dict = {}

	i = 0
	while i < len(codeElements):
		dict[codeElements[i].text] = descElements[i].text
		i += 1

	return json.dumps(dict)

def main():
	# print(scrapeBuildingCodes())
	with open('buildingCodes.txt', 'w+') as f:
		f.writelines(run())
