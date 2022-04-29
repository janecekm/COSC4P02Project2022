import sys
from selenium import webdriver
driver = webdriver.Chrome() # Chnage this when scraping so that it reflects the driver you are using.
def scrapeOfferings(outputfile):
    file = open(outputfile,"w")
    sys.stdout = file
    from web_scraping import offeringScrape
    offeringScrape.run(driver)
    sys.stdout = sys.__stdout__
    file.close()
    print("Offering scrape done")

def cleanOfferings(outputfile,filename):
    file = open(outputfile,"w")
    sys.stdout = file
    from datapreprocessingcode import cleaningtimetable
    cleaningtimetable.run(filename)
    sys.stdout = sys.__stdout__
    file.close()
    print("cleaning scrape done")

def scrapeCleanOfferings(outputfile,filename):
    scrapeOfferings(filename)
    cleanOfferings(outputfile,filename)
