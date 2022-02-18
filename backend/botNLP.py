import spacy
from spacy.matcher import Matcher
from string import Template

nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)

# course codes
courseCaps = [{'IS_ALPHA': True, 'LENGTH': 4},
           {'SHAPE': 'dXdd'}]
courseLower = [{'IS_ALPHA': True, 'LENGTH': 4},
           {'SHAPE': 'dxdd'}]
matcher.add("course code", [courseCaps, courseLower])

# who teaches, who is teaching, who is the instructor, who is the professor
teaching = [{'LOWER': 'who'},
           {'LEMMA': 'be', 'OP': '?'},
           {'LEMMA': 'teach'}]
instructor = [{'LOWER': 'who'},
           {'OP': '?'},
           {'OP': '?'},
           {'LOWER': 'instructor'}]
professor = [{'LOWER': 'who'},
           {'OP': '?'},
           {'OP': '?'},
           {'LOWER': 'professor'}]
matcher.add("instructor", [teaching, instructor, professor])

# when is, when are, what time is
when = [{'LOWER': 'when'},
           {'LEMMA': 'be', "OP": "?"}]
whatTime = [{'LOWER': 'what'},
           {'LOWER': 'time'},
           {'LEMMA': 'be'}]
matcher.add("time", [when, whatTime])

# what are the prereq(uisites)
prerequisites = [{'LOWER': 'what'},
           {'OP': '?'},
           {'OP': '?'},
           {'LEMMA': 'prerequisites'}]
prereqs = [{'LOWER': 'what'},
           {'OP': '?'},
           {'OP': '?'},
           {'LEMMA': 'prereqs'}]
matcher.add("prereqs", [prerequisites, prereqs])

generalTell = [{'LOWER':'tell'},{'LOWER':'me'},{'LOWER':'about'}]
generalInfoOn = [{'LOWER':'information'},{'LOWER':'on'}]
generalInfoOn2 = [{'LOWER':'info'},{'LOWER':'on'}]

matcher.add("general question",[generalTell, generalInfoOn, generalInfoOn2])

openerMatch = [{"LOWER": {"IN": ['hello','hi','hey','howdy','yo','sup','hiya','heyo']}}]

matcher.add("openerGreet", [openerMatch])

progQuestion = [{'LOWER':'the'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'LOWER':'program'}]

matcher.add("program question",[progQuestion])

# course components

courseComp = [{'LEMMA': {"IN": ['sem', 'seminar', 'lab', 'tut', 'tutorial', 'lec', 'lecture']}},
           {'LIKE_NUM': True, 'OP': '?'}]

matcher.add("course component", [courseComp])

# location
where = [{'LOWER': 'where'}]
whatBuilding = [{'LOWER':'what'}, {'LOWER':'building'}]
location = [{'LOWER':'location'}]

matcher.add("location", [where, whatBuilding, location])

# exam
exam = [{'LEMMA':'exam'}]
matcher.add("exam", [exam])

# exists
does = [{'LOWER':'does'}]
matcher.add("exists", [does])


reqQuestion = [{'LOWER':'the'},{'LOWER':'program','OP':'?'},{'LOWER':'requirements'},{'LOWER':'for'}]

matcher.add("requirement question",[reqQuestion])

def extractKeywords(question): 
    doc = nlp(question)
    matches = matcher(doc)
    print(question)
    myString = ""
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # get string rep
        span = doc[start:end]  # matched span
        myString = myString + str(string_id) + " " + str(start) + " " + str(end) + " " + str(span.text) + " "
    return matches

def formResponse(matchedKeys):
    returnThis = ""
    temp = Template("You are asking about $x")
    for match_id, start, end in matchedKeys:
        match_id_ = nlp.vocab.strings[match_id]
        if match_id_ == "openerGreet":
            returnThis += "Hello, world! "
        else: 
            returnThis = temp.substitute({'x': match_id_})
    return returnThis        

def processQ(question):
    matches = extractKeywords(question)
    myString = formResponse(matches)
    print(myString)
    print(type(myString))
    if (myString != "" and myString != None):    
        return {"message": myString}
    else:
         return {"message": "does not compute"}