from queryTables import doQueries
import botNLP
import brockMatcher
from brockMatcher import formResponse
from brockMatcher import matcher,phrase_matcher

botNLP.matcher = matcher
botNLP.phrase_matcher = phrase_matcher
## formQuery testing     #####

def getQueries(question):
    matches, doc = botNLP.extractKeywords(question)
    process = botNLP.processKeywords(matches,doc)
    query = doQueries(process)
    return formResponse(query,matches)

def testing_descriptions_response():
    temp = getQueries("What is VISA 1p95")
    assert "Technical foundations of digital images, media methods and concepts" in temp

def testing_exams_response():
    temp = getQueries("when is econ 2p30 exam")
    assert "April 18 at 14:00-17:00 WCDVIS" in temp

def testing_locations_response():
    temp = getQueries("where is econ 2p30")
    assert "SYNC" in temp or "STH 204" in temp
    temp = getQueries("where is econ 2p30 lec")
    assert "SYNC" in temp or "STH 204" in temp
    temp = getQueries("where is clas 1p97")
    assert "THSOS" in temp

def testing_prereqs_response():
    temp = getQueries("what are the prereqs for entr 2p51")
    assert "no prerequisites" in temp
    temp = getQueries("what are the prereqs for btec 4p06")
    assert "BTEC 3P50, BIOL 3P51" in temp

def testing_instructor_response():
    temp = getQueries("who teaches COSC 4p61")
    assert "Ke" in temp
    temp = getQueries("who teaches VISA 1p95")
    assert "Cerquera Benjumea Gustavo" in temp
    temp = getQueries("who teaches PHIL 2p17")
    assert "Lightbody Brian" in temp
    temp = getQueries("who teaches BIOL 4p06?")
    assert "Ping" in temp

def testing_crosslisting_response():
    temp = getQueries("what crosslisted as COSC 4p61")
    assert "MATH 4P61" in temp
    temp = getQueries("What crosslisted as BIOL 4p06")
    assert "BTEC 4P06" in temp

def testing_links_response():
    temp = getQueries("this is nonense")
    assert "https://brocku.ca/" in temp
    temp = getQueries("where can I get food on campus")
    assert "brocku.ca/dining-services/dining-on-campus/" in temp
    temp = getQueries("how do I get to brock university")
    assert "transitapp.com/" in temp

