from queryTables import doQueries
import botNLP
import brockMatcher
#queryTables.doQuery testing. 

#Course code comparisons are being weird
def testing_doQuery_description():
     matches, doc = botNLP.extractKeywords("What is COSC 1P03?")
     temp = botNLP.processKeywords(matches,doc)
     dict = doQueries(temp)
     print(dict)
     assert dict["code"] == "COSC 1P03" and "Programming and problem solving in a high-level" in dict["description"]


def testing_doQuery_prereqs():
     matches, doc = botNLP.extractKeywords("What are prereqs for COSC 1P03?")
     temp = botNLP.processKeywords(matches,doc)
     dict = doQueries(temp)
     assert dict["code"] == "COSC 1P03" and "COSC 1P02" in dict["prereq"]

def testing_doQuery_xlist():
     matches, doc = botNLP.extractKeywords("What is COSC 4P61 crosslisted as?")
     temp = botNLP.processKeywords(matches,doc)
     dict = doQueries(temp)
     assert dict["code"] == "COSC 4P61" and dict["xlist"] == "MATH 4P61"

def testing_doQuery_validExam():
     matches, doc = botNLP.extractKeywords("When is COSC 1P02 exam?")
     temp = botNLP.processKeywords(matches,doc)
     dict = doQueries(temp)
     assert dict["code"] == "COSC 1P02" and dict["time"] == "14:00-17:00"

def testing_doQuery_examMoreInfo():
     matches, doc = botNLP.extractKeywords("When is COSC exam")
     temp = botNLP.processKeywords(matches,doc)
     dict = doQueries(temp)
     assert not dict

def testing_doQuery_loc():
    matches, doc = botNLP.extractKeywords("where is MCJ")
    temp = botNLP.processKeywords(matches,doc)
    dict = doQueries(temp)
    assert "Mackenzie Chown" in dict['name']

def testing_doQuery_component():
    matches, doc = botNLP.extractKeywords("when is econ 2p30 lab")
    temp = botNLP.processKeywords(matches,doc)
    dict = doQueries(temp)
    assert len(dict)==0 # there is no lab
    
def testing_doQuery_instructor():
    matches, doc = botNLP.extractKeywords("who teaches math 1p66?")
    temp = botNLP.processKeywords(matches, doc)
    dict = doQueries(temp)
    assert dict[0]["instructor"] != (" " or None)