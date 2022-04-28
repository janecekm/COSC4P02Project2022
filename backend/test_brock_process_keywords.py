from queryTables import doQueries
from numpy import extract
from py import process
import botNLP
import brockMatcher
'''
testing for process Keywords
'''
def testing_description_of_course():
    matches, doc = botNLP.extractKeywords("what is cosc 1p03?")#spelt correct
    temp2 = botNLP.processKeywords(matches, doc)
    assert temp2["description"] == "what is" and temp2["code"] =="cosc 1p03"
    matches, doc = botNLP.extractKeywords("WHAT IS COSC 2P03")#all in caps
    temp2 = botNLP.processKeywords(matches,doc)
    assert temp2["description"] == "what is" and temp2["code"] == "cosc 2p03"

def testing_spaces_between_course():
    matches, doc = botNLP.extractKeywords("what are prereq for math1p67?")
    temp = botNLP.processKeywords(matches, doc)
    assert temp["prereq"] == "prereq" and temp["code"] == "math1p67"

def testing_processing_speltwrong():
    matches, doc = botNLP.extractKeywords("what are prereqst for Math 1p67?")
    temp2 = botNLP.processKeywords(matches,doc)
    assert temp2["prereq"] == "prereqs" and temp2["code"] == "math 1p67"

##need to test crosslisting, and need to know how to test it.

def testing_processing_exam():
    matches, doc = botNLP.extractKeywords("where is my cosc 4p32 exam")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["exam"] == "exam" and temp["code"] == "cosc 4p32"

def testing_processing_crosslisting():
    matches, doc = botNLP.extractKeywords("what is COSC 4p61 crosslisted as?")
    temp = botNLP.processKeywords(matches, doc)
    assert temp["xlist"] == "crosslisted" and temp["code"] == "cosc 4p61"
    matches, doc = botNLP.extractKeywords("what are the crosslisting of Cosc 4p61")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["xlist"] == "crosslisting" and temp["code"] == "cosc 4p61"

def testing_processing_location_courses():
    matches, doc = botNLP.extractKeywords("where is cosc 3p98 class")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["location"] == "where" and temp["code"] =="cosc 3p98"

def testing_processing_instructor_courses():
    matches, doc = botNLP.extractKeywords("who teaches math 1p66?")
    temp = botNLP.processKeywords(matches, doc)
    assert temp["instructor"] == "who teaches" and temp["code"] == "math 1p66"

def testing_processing_time_courses():
    matches, doc = botNLP.extractKeywords("when is econ 2p30 class")
    temp = botNLP.processKeywords(matches, doc)
    assert temp["time"] == "when is" and temp["code"] == "econ 2p30"

def testing_processing_time_courses_lab():
    matches, doc = botNLP.extractKeywords("when is econ 2p30 lab")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["format"] == "lab" and temp["time"] == "when is" and temp["code"] == "econ 2p30"

def testing_processing_building():
    matches, doc = botNLP.extractKeywords("where is MCJ")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["buildingCode"] == "mcj"
    matches, doc = botNLP.extractKeywords("How can I get to MCD")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["buildingCode"] == "mcd"
    matches, doc = botNLP.extractKeywords("where is mcd 205")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["buildingCode"] == "mcd"
    matches, doc = botNLP.extractKeywords("where is mcd205")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["buildingCode"] == "mcd"

def testing_programName():
    matches, doc = botNLP.extractKeywords("tell me more about accounting")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["programName"] == "accounting"
    matches, doc = botNLP.extractKeywords("tell me about Mathematics program at brock")
    temp = botNLP.processKeywords(matches, doc)
    assert temp["programName"] == "mathematics"
