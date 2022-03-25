import json
from selenium import webdriver
from selenium.webdriver.common.by import By


'''
Returns json that looks like:
	1 - occasion name
	2 - term
	3 - type
	4 - date

I had to do this because the source doesn't have attribute fields, wtf.
'''

def getDates():
	driver = webdriver.Chrome()
	driver.get("https://brocku.ca/important-dates/all/")

	items = driver.find_elements(By.XPATH, '//table[@class="gsheets"]/tbody/tr/td')

	counter = 1
	dict = {}

	for i in items:

		dict[counter] = i.text
		if counter % 4 == 0: #every 4 td fields is a complete row in the table
			print(json.dumps(dict))
			counter = 1
			dict = {}

		else:
			counter += 1



def main():
	getDates()


main()
