from queryTables import doQueries
from numpy import extract
from py import process
import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import botNLP

error_message_1 = "I'm sorry, I wasn't able to find what you were looking for. However, you might be able to find more information at: https://brocku.ca/"
error_message_2 = "I am not quite sure what you're asking. Could you rephrase that?"
#botNLP.ProcessQ
def testing_invalid_input_ProcessQ():
    assert (botNLP.processQ('raietweiaweeiiwnaeiugwe')['message'] == error_message_1) or (botNLP.processQ('raietweiaweeiiwnaeiugwe')['message'] == error_message_2)
def testing_valid_input_ProcessQ():
    assert 'COSC 1P02' in botNLP.processQ('What is the prereqs for COSC 1P03')['message']
def testing_valid_misspelled_input_ProcessQ():
    assert 'COSC 1P02' in botNLP.processQ('What aer the Prereq for COSC 1p03')['message']
def testing_valid_more_misspelled_input_ProcessQ():
    assert (botNLP.processQ('Qjtat is jet prereq for COSC 1p03')['message'] == error_message_2) or (botNLP.processQ('Qjtat is jet prereq for COSC 1p03')['message'] == error_message_1)
def testing_misspelled_wat_input_ProcessQ():
    assert 'COSC 1P02' in botNLP.processQ('Wat is prereqs for COSC 1P03')['message'] 
def testing_attempt_SQL_injection1_ProcessQ():
    assert (botNLP.processQ('What are the prereqs for *’-- 1P02')['message'] == error_message_1) or (botNLP.processQ('What are the prereqs for *’-- 1P02')['message'] == error_message_2)
def testing_attempt_SQL_injection2_ProcessQ():
    assert (botNLP.processQ('What are the prereqs for /**/ *’--')['message'] == error_message_1) or (botNLP.processQ('What are the prereqs for /**/ *’--')['message'] == error_message_2) 
def testing_single_hello_processQ():
    assert botNLP.processQ('Hello Hello')['message']== "Hello"

def testing_spacefor_course():
    assert 'MATH 1P66' in botNLP.processQ("what are prereq for math1p67")['message']

#botNLP.getLink
def testing_prereq_getLink():
    assert 'https://brocku.ca/webcal/undergrad/' in botNLP.getLink('prereq')


#botNLP.extractKeywords - TESTING matcher hash correctness and positional matching
'''
MATCHER can do 
crosslist
generalInfo
time                          8885804376230376864    ---> Why is time returned backwards? 
instructor                    8794063152469658309 
prereqs      "what is prereq" 12246778916035409871
xlist                         12057252092477718455
course code                   3084953006211575075
description    "what is"      15699362302781265145
openergreet "hello/hi/hey"    13357464451824626592
course component              8383911667181403691

location                      4272944830542554761
exam                          9704506296879342145
advisor                       13790784326572561368
covid                        2127825066894192516
tuition                      1002886381125543945
food                         18057327756930201825
transport                    18207339096255186229
register                     507029484556359861
directory
store                        7338335557000497525
'''
def testing_extract_keywords_course():
    response = botNLP.extractKeywords("What is COSC 1P03?")
    assert response[0][0] == (15699362302781265145, 0,2) and response[0][1] == (3084953006211575075, 2, 4)
    '''
    WHAT IS and COURSE is [(15699362302781265145, 0,2), (3084953006211575075, 2, 4)]
    '''

#can it match regardless of position? 
def testing_extract_keywords_course_backwards():
    response = botNLP.extractKeywords("COSC 1P03 what is")
    assert response[0][1] == (15699362302781265145, 2,4) and response[0][0] == (3084953006211575075, 0, 2)

#need matcher hash codes uhm
def testing_extract_keywords_crosslist():
    response = botNLP.extractKeywords("what is COSC 1P02 crosslist")
    print(response)

def testing_extract_keywords_prereqs():
    response = botNLP.extractKeywords("What is prereqs for COSC 1P03?")
    assert response[0][0] == (15699362302781265145, 0,2) and response[0][1] == (12246778916035409871, 0, 3) and response[0][2] == (3084953006211575075, 4, 6)

def testing_extract_keywords_hello():
    response = botNLP.extractKeywords("Hello")
    assert response[0][0] == (13357464451824626592, 0, 1)

def testing_extract_keywords_instructor():
    response = botNLP.extractKeywords("Who is teaching COSC 4P03?")
    assert response[0][0] == (8794063152469658309, 0, 3) and response[0][1] == (3084953006211575075, 3, 5)

def testing_extract_keywords_time():
    response = botNLP.extractKeywords("What time is MUSI 3P99?")
    assert response[0][0] == (3084953006211575075, 3, 5) and response[0][1] == (8885804376230376864, 0, 3)

def testing_extract_keywords_lab():
    response = botNLP.extractKeywords("When is lab for COSC 1P02?")
    assert (8383911667181403691, 2, 3) in response[0]

def testing_extract_keywords_tutorial():
    response = botNLP.extractKeywords("When is tutorial for COSC 1P02?")
    assert (8383911667181403691, 2, 3) in response[0]

def testing_extract_keywords_lecture():
    response = botNLP.extractKeywords("When is lecture for COSC 1P03?")
    assert (8383911667181403691, 2, 3) in response[0]

def testing_extract_keywords_loc():
    response = botNLP.extractKeywords("Where is CHEM 1P02 lecture?")
    print(response)
    assert (4272944830542554761, 0, 1) in response[0]

def testing_extract_keywords_exam():
    response = botNLP.extractKeywords("When is MATH 1P06 exam?")
    print(response)
    assert (8885804376230376864, 0, 2) in response[0] and (9704506296879342145, 4, 5) in response[0]

def testing_extract_keywords_advisor():
    response = botNLP.extractKeywords("Who is the advisor for math?")
    assert (13790784326572561368, 3, 4) in response[0]

def testing_extract_keywords_transit():
    response = botNLP.extractKeywords("Where is the bus?")
    assert (18207339096255186229, 3, 4) in response[0]

def testing_extract_keywords_transit():
    response = botNLP.extractKeywords("How do I get to Welland?") #of all places
    assert (18207339096255186229, 0, 5) in response[0] #Ah, the whole phrase of type "how do I get to" is a match

def testing_extract_keywords_weird_transit():
    response = botNLP.extractKeywords("How do I get to Narnia?") #if that's the case then...this should work? 
    assert (18207339096255186229, 0, 5) in response[0]

def testing_extract_keywords_weird_transit():
    response = botNLP.extractKeywords("Does the bus go to Narnia?") 
    assert (18207339096255186229, 2, 3) in response[0]

def testing_extract_keywords_register():
    response = botNLP.extractKeywords("How do I register for courses?")
    assert (507029484556359861, 3, 4) in response[0]

def testing_extract_keywords_store():
    response = botNLP.extractKeywords("campus store?")
    assert (7338335557000497525, 1, 2) in response[0]

def testing_extract_keywords_books():
    response = botNLP.extractKeywords("Where do I buy textbooks?")
    assert (7338335557000497525, 4, 5) in response[0]

def testing_extract_keywords_food():
    response = botNLP.extractKeywords("Where can I eat?")
    assert (18057327756930201825,3,4) in response[0]

def testing_extract_keywords_food2():
    response = botNLP.extractKeywords("Where can I buy food?")
    assert (18057327756930201825,4,5) in response[0]

def testing_extract_keywords_covid():
    response = botNLP.extractKeywords("What are the covid rules at Brock?")
    assert (2127825066894192516,3,4) in response[0]

def testing_extract_keywords_vaccine():
    response = botNLP.extractKeywords("Do I need a covid vaccine?")
    assert (2127825066894192516,4,5) in response[0]

def testing_extract_keywords_tuition():
    response = botNLP.extractKeywords("How do I pay tuition?")
    assert (1002886381125543945, 4,5) in response[0]

def testing_extract_keywords_tuition2():
    response = botNLP.extractKeywords("How much is tuition?")
    assert (1002886381125543945, 3,4) in response[0]


def testing_extract_keywords_xlist():
    response = botNLP.extractKeywords("What is crosslist for COSC 4P61?")
    assert (12057252092477718455, 0,3) in response[0]

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
     assert dict == 'more info required' or dict == 'placeholder return'

def testing_doQuery_loc():
    matches, doc = botNLP.extractKeywords("where is MCJ")
    temp = botNLP.processKeywords(matches,doc)
    dict = doQueries(temp)
    assert "Mackenzie Chown" in dict

def testing_doQuery_component():
    matches, doc = botNLP.extractKeywords("when is econ 2p30 lab")
    temp = botNLP.processKeywords(matches,doc)
    dict = doQueries(temp)
    assert dict["code"] == "ECON 2P30" and dict["course component"] == "lab" and dict["time"] != None
    
def testing_doQuery_instructor():
    matches, doc = botNLP.extractKeywords("who teaches math 1p66?")
    temp = botNLP.processKeywords(matches, doc)
    dict = doQueries(temp)
    assert dict["instructor"] != (" " or None)
## formQuery testing     #####

def getQueries(question):
    matches, doc = botNLP.extractKeywords(question)
    process = botNLP.processKeywords(matches,doc)
    query = doQueries(process)
    return botNLP.formResponse(query,matches)

def testing_exams_response():
    temp = getQueries("when is econ 2p30 exam")
    assert "April 18 at 14:00-17:00 WCDVIS" in temp

def testing_locations_response():
    temp = getQueries("where is econ 2p30")
    assert "ST 107" in temp
    temp = getQueries("where is clas 1p97")
    assert "THSOS" in temp

def testing_prereqs_response():
    temp = getQueries("what are the prereqs for entr 2p51")
    assert "no prerequisites" in temp
    temp = getQueries("what are the prereqs for btec 4p06")
    assert "BTEC 3P50, BIOL 3P51" in temp

def testing_instructor_response():
    temp = getQueries("who teaches VISA 1p95")
    assert "Cerquera Benjumea, Gustavo" in temp
    temp = getQueries("who teaches PHIL 2p17")
    assert "Lightbody, Brian" in temp
    temp = getQueries("who teaches BIOL 4p06?")
    assert "Liang, Ping" in temp

def testing_crosslisting_response():
    temp = getQueries("Biol 4p06 crosslisting")
    assert "BTEC 4P06" in temp

def testing_links_response():
    temp = getQueries("this is nonense")
    assert "https://brocku.ca/" in temp
    temp = getQueries("where can I get food on campus")
    assert "brocku.ca/dining-services/dining-on-campus/" in temp
    temp = getQueries("how do I get to brock university")
    assert "transitapp.com/" in temp


##testing autocorrection
def correcting_english(question):
    nlp = spacy.load("en_core_web_md")
    matcher = Matcher(nlp.vocab)
    phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    doc = nlp(question)
    matches = matcher(doc)
    phrases_matched = phrase_matcher(doc)
    for match in phrases_matched:
        matches.append(match)
    return botNLP.spellcheck(question,matches,doc)

def testing_spelling_mistake():
    matches, docs = correcting_english("hello there")
    print(matches)
    print(docs)
