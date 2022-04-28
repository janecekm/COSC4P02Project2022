from queryTables import doQueries
from numpy import extract
from py import process
import botNLP
import brockMatcher
#botNLP.extractKeywords - TESTING matcher hash correctness and positional matching
'''
MATCHER can do 
crosslist                       3084953006211575075
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
    assert response[0][1] == (15699362302781265145, 0, 2)
    '''
    WHAT IS and COURSE is [(15699362302781265145, 0,2), (3084953006211575075, 2, 4)]
    '''

#can it match regardless of position? 
def testing_extract_keywords_course_backwards():
    response = botNLP.extractKeywords("COSC 1P03 what is")
    assert response[0][1] == (10779227342117629034, 2,3) and response[0][0] == (3084953006211575075, 0, 2)

#need matcher hash codes uhm
def testing_extract_keywords_crosslist():
    response = botNLP.extractKeywords("what is COSC 1P02 crosslist")
    assert response[0][2] == (3084953006211575075,2,4)

def testing_extract_keywords_prereqs():
    response = botNLP.extractKeywords("What is prereqs for COSC 1P03?")
    print(response)
    assert response[0][1] == (15699362302781265145, 0, 2)

def testing_extract_keywords_hello():
    response = botNLP.extractKeywords("Hello")
    assert response[0][0] == (13357464451824626592, 0, 1)

def testing_extract_keywords_instructor():
    response = botNLP.extractKeywords("Who is teaching COSC 4P03?")
    assert response[0][1] == (8794063152469658309, 0, 3) and response[0][0] == (10779227342117629034, 0, 1)

def testing_extract_keywords_time():
    response = botNLP.extractKeywords("What time is MUSI 3P99?")
    assert response[0][1] == (3084953006211575075, 3, 5) and response[0][0] == (10779227342117629034, 0, 1)

def testing_extract_keywords_lab():
    response = botNLP.extractKeywords("When is lab for COSC 1P02?")
    assert (8885804376230376864, 0, 2) in response[0]

def testing_extract_keywords_tutorial():
    response = botNLP.extractKeywords("When is tutorial for COSC 1P02?")
    assert (8885804376230376864, 0, 2) in response[0]

def testing_extract_keywords_lecture():
    response = botNLP.extractKeywords("When is lecture for COSC 1P03?")
    assert (8885804376230376864, 0, 2) in response[0]

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
    print(response)
    assert (10779227342117629034, 0,1) in response[0]