import spacy
from spacy.matcher import Matcher
from string import Template

nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)

# course codes
courseCode = [[{'IS_ALPHA': True, 'LENGTH': 4},
               {'SHAPE': 'dxdd'}],
             [{"SHAPE":  "xxxxdxdd"}]]
matcher.add("course code", courseCode)

# who teaches, who is teaching, who is the instructor, who is the professor
teaching = [[{'LOWER': 'who'},
            {'LEMMA': 'be', 'OP': '?'},
            {'LEMMA': 'teach'}],
           [{'LOWER': 'who'},
            {'OP': '?'},
            {'OP': '?'},
            {'LOWER': 'instructor'}],
           [{'LOWER': 'who'},
            {'OP': '?'},
            {'OP': '?'},
            {'LOWER': 'professor'}]]
matcher.add("instructor", teaching)

# when is, when are, what time is
when = [[{'LOWER': 'when'},
         {'LEMMA': 'be', "OP": "?"}],
        [{'LOWER': 'what'},
         {'LOWER': 'time'},
         {'LEMMA': 'be'}]]
matcher.add("time", when, greedy="LONGEST")

# what are the prereq(uisites)
prerequisites = [[{'LOWER': 'what'},
                  {'OP': '?'},
                  {'OP': '?'},
                  {'LEMMA': 'prerequisites'}], 
                [{'LOWER': 'what'},
                  {'OP': '?'},
                  {'OP': '?'},
                  {'LEMMA': 'prereqs'}]]
matcher.add("prereqs", prerequisites)


generalInfo = [ [{'LOWER':'tell'},{'LOWER':'me'},{'LOWER':'about'}], 
                [{'LOWER':'information'},{'LOWER':'on'}],
                [{'LOWER':'info'},{'LOWER':'on'}]]

matcher.add("general question", generalInfo)

openerMatch = [{"LOWER": {"IN": ['hello','hi','hey','howdy','yo','sup','hiya','heyo']}}]

matcher.add("openerGreet", [openerMatch])

progQuestion = [{'LOWER':'the'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'LOWER':'program'}]

matcher.add("program question",[progQuestion])

# course components
courseComp = [{'LEMMA': {"IN": ['sem', 'seminar', 'lab', 'tut', 'tutorial', 'lec', 'lecture']}},
           {'LIKE_NUM': True, 'OP': '?'}]

matcher.add("course component", [courseComp], greedy="LONGEST")

# location
location = [[{'LOWER':'location'}],
            [{'LOWER':'what'}, {'LOWER':'building'}], 
            [{'LOWER': 'where'}]]

matcher.add("location", location)

# exam
exam = [{'LEMMA':'exam'}]
matcher.add("exam", [exam])

# exists
does = [{'LOWER':'does'}]
matcher.add("exists", [does])

reqQuestion = [{'LOWER':'the'},{'LOWER':'program','OP':'?'},{'LOWER':'requirements'},{'LOWER':'for'}]

matcher.add("requirement question",[reqQuestion])

# You are asking about the _________ of __________
# type/amount of information -- general info, or time, or location
# finer detail -- course code or course component

# span's custom attributes // attribute extensions ._.
# matcher callback function on_match=function()

def extractKeywords(question): 
    question = question.lower() # make question lowercase 
    doc = nlp(question)
    matches = matcher(doc)
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
            if returnThis.__contains__("You are asking about"):
                returnThis += ", " + match_id_
            else:
                returnThis += temp.substitute({'x': match_id_})
    return returnThis

def processQ(question):
    matches = extractKeywords(question)
    myString = formResponse(matches)
    print(myString)
    print(type(myString))
    if (myString != "" and myString != None):    
        return {"message": myString}
    else:
         return {"message": "I am not quite sure what you're asking. Could you rephrase that?"}