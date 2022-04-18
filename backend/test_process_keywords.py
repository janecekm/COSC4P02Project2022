from queryTables import doQueries
from numpy import extract
from py import process
import botNLP
'''
testing for process Keywords
'''
def testing_description_of_course():
    matches, doc = botNLP.extractKeywords("what is cosc 1p03?")#spelt correct
    temp2 = botNLP.processKeywords(matches, doc)
    assert temp2["description"].text == "what is" and temp2["code"].text =="cosc 1p03"
    matches, doc = botNLP.extractKeywords("WHAT IS COSC 2P03")#all in caps
    temp2 = botNLP.processKeywords(matches,doc)
    assert temp2["description"].text == "what is" and temp2["code"].text == "cosc 2p03"

def testing_spaces_between_course():
    matches, doc = botNLP.extractKeywords("what are prereq for math1p67?")
    temp = botNLP.processKeywords(matches, doc)
    assert temp["prereq"].text == "what are prereq" and temp["code"].text == "math 1p67"

def testing_processing_speltwrong():
    matches, doc = botNLP.extractKeywords("what are prereq for Math 1p67?")
    temp2 = botNLP.processKeywords(matches,doc)
    assert temp2["prereq"].text == "what are prereq" and temp2["code"].text == "math 1p67"

##need to test crosslisting, and need to know how to test it.

def testing_processing_exam():
    matches, doc = botNLP.extractKeywords("where is my cosc 4p32 exam")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["exam"].text == "exam" and temp["code"].text == "cosc 4p32"

def testing_processing_crosslisting():
    matches, doc = botNLP.extractKeywords("what is COSC 4p61 crosslisted as?")
    temp = botNLP.processKeywords(matches, doc)
    assert temp["xlist"].text == "crosslisted" and temp["code"].text == "cosc 4p61"
    matches, doc = botNLP.extractKeywords("what are the crosslisting of Cosc 4p61")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["xlist"].text == "crosslisted" and temp["code"].text == "cosc 4p61"

def testing_processing_location_courses():
    matches, doc = botNLP.extractKeywords("where is cosc 3p98 class")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["location"].text == "where" and temp["code"].text =="cosc 3p98"

def testing_processing_instructor_courses():
    matches, doc = botNLP.extractKeywords("who teaches math 1p66?")
    temp = botNLP.processKeywords(matches, doc)
    assert temp["instructor"].text == "who teaches" and temp["code"].text == "math 1p66"

def testing_processing_time_courses():
    matches, doc = botNLP.extractKeywords("when is econ 2p30 class")
    temp = botNLP.processKeywords(matches, doc)
    assert temp["time"].text == "when is" and temp["code"].text == "econ 2p30"

def testing_processing_time_courses_lab():
    matches, doc = botNLP.extractKeywords("when is econ 2p30 lab")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["course component"].text == "lab" and temp["time"].text == "when is" and temp["code"].text == "econ 2p30"

def testing_processing_building():
    matches, doc = botNLP.extractKeywords("where is MCJ")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["location"].text == "where" and temp["buildingCode"].text == "mcj"
    matches, doc = botNLP.extractKeywords("How can I get to MCD")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["buildingCode"].text == "mcd"
    matches, doc = botNLP.extractKeywords("where is mcd 205")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["buildingCode"].text == "mcd"
    matches, doc = botNLP.extractKeywords("where is mcd205")
    temp = botNLP.processKeywords(matches,doc)
    assert temp["buildingCode"].text == "mcd"

