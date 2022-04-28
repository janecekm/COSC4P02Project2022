from spacy.tokens import Span
import os
import json
from botNLP import nlp
from spacy.matcher import Matcher,PhraseMatcher
from string import Template
from botNLP import filepath
matcher = Matcher(nlp.vocab)
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
###########################
# This section defines patterns and callback functions for the PhraseMatcher
buildings = []
buildingNames =[]
with open(filepath()+"buildingCodesClean.txt", encoding="utf8") as f: 
    for line in f:
        obj = json.loads(line)
        buildings.append(obj["buildingCode"])
        buildingNames.append(obj["buildingName"])
patterns = list(nlp.pipe(buildings))
phrase_matcher.add("buildingCode", patterns)
patterns = list(nlp.pipe(buildingNames))
phrase_matcher.add("buildingNames", patterns)

def disambiguateProgram(matcher, doc, i, matches): 
    '''Callback function for phrase matcher. Removes overlapping programName matches, keeps longest match
    Ex. "computer science" and "science" are both matches, removes "science" from the match list
    '''
    max_len_match = (-1, -1) # idx, len
    idx = 0
    for match_id, start, end in matches:
        print(idx, nlp.vocab.strings[match_id], doc[start:end]) 
        if nlp.vocab.strings[match_id] == "programName": 
            l = end - start
            if l > max_len_match[1]: 
                if max_len_match[0] != -1:
                    matches.pop(max_len_match[0]) # remove the shorter program from the match list
                max_len_match = (idx, end-start) # update max
            else: 
                matches.pop(idx) # remove the shorter program from the match list
        idx += 1      

programNames = []
with open(filepath()+"program-links.txt", encoding="utf8") as f:
    for line in f: 
        obj = json.loads(line)
        programNames.append((list(obj.keys())[0]))
    patterns = list(nlp.pipe(programNames))
    phrase_matcher.add("programName", patterns, on_match=disambiguateProgram)

###################################
# This section defines all the patterns for the Matcher

# if extension has not been set, create extension
if not Span.has_extension("prio"): 
    Span.set_extension("prio", default=100)

def assignPriority(matcher, doc, i, matches): 
    '''Assigns a priority value to the matched spans. Priority values indicate the importance of the question component. 
    Lower values indicate higher priority. 
    '''
    match_id, start, end = matches[i]
    if match_id == nlp.vocab.strings["openerGreet"]\
        or match_id == nlp.vocab.strings["question"]:
        doc[start:end]._.prio = 3
    elif match_id == nlp.vocab.strings["code"] \
        or match_id == nlp.vocab.strings["format"] \
        or match_id == nlp.vocab.strings["buildingCode"] :
        doc[start:end]._.prio = 2
    elif match_id == nlp.vocab.strings["description"]: 
        doc[start:end]._.prio = 1
    else: # every other question term is more specific so it is highest prio
        doc[start:end]._.prio = 0

# course codes -- course/offering/exam 
courseCode = [[{'IS_ALPHA': True, 'LENGTH': 4},
              {'SHAPE': {'IN': ['dxdd', 'dXdd']}}],
            [{"SHAPE":  {'IN': ["xxxxdxdd", "Xxxxdxdd", "xXxxdxdd", "XXxxdxdd", "xxXxdxdd", "XxXxdxdd", "xXXxdxdd", "XXXxdxdd", "xxxXdxdd",
            "XxxXdxdd", "xXxXdxdd", "XXxXdxdd", "xxXXdxdd", "xXXXdxdd", "XXXXdxdd", "xxxxdXdd", "XxxxdXdd", "xXxxdXdd", "XXxxdXdd", "xxXxdXdd",
            "XxXxdXdd", "xXXxdXdd", "xxxXdXdd", "XxxXdXdd", "xXxXdXdd", "XXxXdXdd", "xxXXdXdd", "XxXXdXdd", "xXXXdXdd", "XXXXdXdd" ]}}]]
matcher.add("code", courseCode, on_match=assignPriority)

# who teaches, who is teaching, who is the instructor, who is the professor
# offering table
teaching = [[{'LOWER': 'who'},
            {'LEMMA': 'be', 'OP': '?'},
            {'LEMMA': 'teach'}],
          [{'LOWER': 'who'},
            {'OP': '*'},
            {'LOWER': 'instructor'}],
          [{'LOWER': 'who'},
            {'OP': '*'},
            {'LOWER': 'professor'}],
          [{'LOWER': 'who'},
            {'OP': '*'},
            {'LOWER': 'prof'}]]
matcher.add("instructor", teaching, on_match=assignPriority)

# when is, when are, what time is
when = [[{'LOWER': 'when'},
        {'LEMMA': 'be', "OP": "?"}],
        [{'LOWER': 'what'},
        {'LOWER': 'time'},
        {'LEMMA': 'be'}]]
matcher.add("time", when, greedy="LONGEST", on_match=assignPriority)

# question
question = [[{'LOWER': 'who'}], 
                [{'LOWER': 'what'}],
                [{'LOWER': 'when'}],
                [{'LOWER': 'where'}], 
                [{'LOWER': 'why'}]]
matcher.add("question", question, on_match=assignPriority)

# what are the prereq(uisites) -- course table
prerequisites = [[{'LEMMA': 'prerequisite'}], 
                [{'LEMMA': 'prereq'}]]
matcher.add("prereq", prerequisites, on_match=assignPriority)

crosslist = [[{'LOWER': 'crosslist'}], 
                [{'LOWER': 'crosslisted'}], 
                [{'LEMMA': 'crosslisting'}], 
                [{'LOWER': 'what'},
                  {'OP': '?'},
                  {'OP': '?'},
                  {'LEMMA': 'xlist'}]]
matcher.add("xlist", crosslist, on_match=assignPriority)

# general descriptions
generalInfo = [ [{'LOWER':'tell'},{'LOWER':'me'},{'LOWER':'about'}], 
                [{'LOWER':'information'},{'LOWER':'on'}],
                [{'LOWER':'info'},{'LOWER':'on'}], 
                [{'LOWER': 'what'}, {'LOWER': 'is'}]]
matcher.add("description", generalInfo, on_match=assignPriority)

openerMatch = [{"LOWER": {"IN": ['hello','hi','hey','howdy','yo','sup','hiya','heyo']}}]
matcher.add("openerGreet", [openerMatch], on_match=assignPriority)

# don't have table
progQuestion = [{'LOWER':'the'},{'OP':'*'},{'LOWER':'program'}]
matcher.add("program question",[progQuestion], on_match=assignPriority)

# formats -- offering table
courseComp = [{'LEMMA': {"IN": ['sem', 'seminar', 'lab', 'tut', 'tutorial', 'lec', 'lecture', 'sec', 'section']}},
          {'LIKE_NUM': True, 'OP': '?'}]
matcher.add("format", [courseComp], greedy="LONGEST", on_match=assignPriority)

# location -- offering or exam
location = [[{'LOWER':'location'}],
            [{'LOWER':'what'}, {'LOWER':'building'}], 
            [{'LOWER': 'where'}]]
matcher.add("location", location, on_match=assignPriority)

# exam table
exam = [{'LEMMA':'exam'}]
matcher.add("exam", [exam], on_match=assignPriority)

reqQuestion = [{'LOWER':'the'},{'LOWER':'program','OP':'?'},{'LOWER':'requirements'},{'LOWER':'for'}]

matcher.add("requirement question",[reqQuestion], on_match=assignPriority)

# advisor table
advisor = [{'LEMMA':'advisor'}]
matcher.add("advisor", [advisor], on_match=assignPriority)

# covid information
covid = [[{'LOWER':'covid'}],[{'LOWER':'covid19'}],[{'LOWER':'covid-19'}]
            ,[{'LOWER':'coronavirus'}],[{'LOWER':'quarantine'}],[{'LOWER':'lockdown'}]]
matcher.add("covid", covid, on_match=assignPriority)

# tuition
tuition = [[{'LEMMA':'cost'}],[{'LOWER':'tuition'}],[{'LEMMA':'price'}],[{'LOWER':'money'}],[{'LEMMA':'dollar'}],
            [{'LEMMA':'pay'}]]
matcher.add("tuition", tuition, on_match=assignPriority)

# food
food = [[{'LEMMA':'eat'}],[{'LOWER':'food'}],[{'LOWER':'breakfast'}],[{'LOWER':'lunch'}],[{'LOWER':'dinner'}],
            [{'LOWER':'meal'}],[{'LOWER':'mealplan'}],[{'LEMMA':'dining'}],[{'LEMMA':'snack'}]]
matcher.add("food", food, on_match=assignPriority)

# transportation, "How do I get to..."
transport = [[{'LEMMA':'transit'}],[{'LEMMA':'travel'}],[{'LEMMA':'bus'}],[{'LEMMA':'transport'}],[{'LEMMA':'transportation'}],
                [{'LOWER': 'how'},
                  {'OP': '*'},
                  {'LEMMA': 'get'},
                  {'LEMMA': 'to'}]]
matcher.add("transport", transport, on_match=assignPriority)

# registration
register = [[{'LEMMA':'register'}],[{'LEMMA':'registration'}],
                [{'LOWER': 'choose'},{'OP': '?'},{'LEMMA': 'class'},],
                [{'LOWER': 'pick'},{'OP': '?'},{'LEMMA': 'class'},],
                [{'LOWER': 'choose'},{'OP': '?'},{'LEMMA': 'classes'},],
                [{'LOWER': 'pick'},{'OP': '?'},{'LEMMA': 'classes'},]]
matcher.add("register", register, on_match=assignPriority)

# directory
directory = [[{'LEMMA':'contact'}], [{'LOWER':'call'}], [{'LOWER':'phone'}], 
            [{'LOWER':'email'}], [{'LEMMA': 'speak'},{'LOWER': 'to'},]]
matcher.add("directory", directory, on_match=assignPriority)

# masters
masters = [[{'LOWER':'graduate'}, {'LOWER':"program"}], 
            [{'LOWER':'graduate'}, {'LOWER':"studies"}], 
            [{'LOWER':'masters'}], [{'LOWER':'msc'}], 
            [{'LOWER':'mba'}], [{'LOWER': 'ma'}], [{'LOWER':'macc'}], [{'LOWER':'mag'}]
            ,[{'LOWER':'mbe'}], [{'LOWER':'mph'}]]
matcher.add("masters", masters, on_match=assignPriority)

# accessible washrooms
a_washrooms = [[{'LOWER':'accessible'}, {'LEMMA':"washroom"}],
    [{'LOWER':'accessible'}], [{'LEMMA':'bathroom'}]]
matcher.add("a_washrooms", a_washrooms, on_match=assignPriority)

# admissions
admission = [[{'LEMMA':'apply'}], 
            [{'LEMMA':'admit'}], [{'LEMMA':'addmission'}] ]
matcher.add("admission", admission, on_match=assignPriority)

# store
store = [[{'LOWER':'store'}], [{'LEMMA':'textbook'}], [{'LEMMA':'booklist'}]]
matcher.add("store", store, on_match=assignPriority)

# end of Matcher pattern defintions

links = {
    "a_washrooms":"https://brocku.ca/blogs/campus-map/category/brock-university/accessibility/accessibility-washrooms",
    "prereqs" : "https://brocku.ca/webcal/undergrad/",
    "exam" : "https://brocku.ca/guides-and-timetables/exams/#more-exam-info",
    "timetable" : "https://brocku.ca/guides-and-timetables/timetables/",
    "brock" : "https://brocku.ca/", 
    "acad_advisor": "https://brocku.ca/academic-advising/find-your-advisor/",
    "tuition" : "https://brocku.ca/safa/tuition-and-fees/overview/", 
    "covid" : "https://brocku.ca/coronavirus/", 
    "food": "https://brocku.ca/dining-services/dining-on-campus/locations-on-campus-and-hours-of-operation/",
    "register" : "https://discover.brocku.ca/registration/",
    "transit" : "https://transitapp.com/region/niagara-region",
    "directory":"https://brocku.ca/directory/", 
    "store":"https://campusstore.brocku.ca/",
    "masters":"https://brocku.ca/programs/graduate/",
    "admission":"https://brocku.ca/admissions/",
    "map": "https://brocku.ca/blogs/campus-map/"
}

# getLink method for the relevant links for Brock
def getLink(matchedKeys):
    '''A method for if the info was not found in the database
    Args: 
        matchedKeys: the list of matches produced from extractKeywords 
                     [(match_id, start, end)]
                      match_id is a hashed value representing the type of match 
                      start is the start index of the matched span (set of tokens)
                      end is the end index of the matched span (set of tokens)
    Return: 
        returns a string to output as a response
    '''
    temp = Template("I'm sorry, I wasn't able to find what you were looking for. However, you might be able to find more information at: $x ")
    # for queries that we will exclusively be giving links to 
    temp2 = Template("Information regarding $y can be found at: $x")

    matches = []
    for match_id, start, end in matchedKeys:
        print(nlp.vocab.strings[match_id])
        matches.append(nlp.vocab.strings[match_id])
    if "prereq" in matches:
        return temp.substitute({'x': links["prereqs"]})
    elif "a_washrooms" in matches:
        return temp2.substitute({'y' : "the accesible washrooms at Brock", 'x': links["a_washrooms"]})
    elif "admission" in matches:
        return temp2.substitute({'y' : "the Brock admissions", 'x': links["store"]})
    elif "store" in matches:
        return temp2.substitute({'y' : "the Brock Campus Store", 'x': links["store"]})
    elif "masters" in matches:
        return temp2.substitute({'y' : "Brock's graduate programs", 'x': links["masters"]})
    elif "directory" in matches:
        return temp2.substitute({'y' : "contacting individuals at Brock", 'x': links["directory"]})
    elif "food" in matches:
        return temp2.substitute({'y' : "the dining options at Brock", 'x': links["food"]})
    elif "transport" in matches:
        return temp2.substitute({'y' : "local public transportation", 'x': links["transit"]})
    elif "covid" in matches:
        return temp2.substitute({'y' : "Brock's COVID-19 response", 'x': links["covid"]})
    elif "register" in matches:
        return temp2.substitute({'y' : "Brock's registration process", 'x': links["register"]})
    elif "advisor" in matches:
        return temp2.substitute({'y' : "academic advisors", 'x': links["acad_advisor"]})
    elif "exam" in matches:
        return temp.substitute({'x': links["exam"]})
    elif "format" in matches or "course code" in matches:
        return temp.substitute({'x': links["timetable"]})
    elif "tuition" in matches:
        return temp2.substitute({'y' : "tuition", 'x': links["tuition"]})
    elif "buildingNames" in matches: 
        return temp2.substitute({'y': "locations on campus", 'x': links["map"]})
    elif "openerGreet" in matches:
        return "What can I help you with today?"
    else:
        return temp.substitute({'x': links["brock"]})

def formResponse(database_answer, keys):
    '''A method to form a response given the database answer and the matched keywords
    Args: 
        database_answer: response from the database, will be of type dictionary, list or None if no response from database
        keys: the list of match info as a result of processing
    Return: 
        a string to output as a response, or None if no response is generated (something unexpected happened)
    '''
    if not database_answer:
        return getLink(keys)
    if "buildingCode" in database_answer:
        temp = Template("$c is the building code for $n. For more details see $l.")
        return temp.substitute({'c':database_answer["buildingCode"], 'n':database_answer["name"], 'l':"https://brocku.ca/blogs/campus-map/"})
    if "exam" in database_answer:
        temp = Template("$c has an exam on $m $d at $t $l")
        return temp.substitute({'c': database_answer["code"], 'm':database_answer["month"], 'd':database_answer["dayNum"], 't':database_answer["time"], 'l':database_answer["location"]})
    # basic response for course descriptions
    if "description" in database_answer: 
        temp = Template("$c is $t and it's about $d")
        return temp.substitute({'c':database_answer["code"], 't':database_answer["title"], 'd':database_answer["description"]})
    if "xlist" in database_answer:
        if database_answer["xlist"] != "":
            temp = Template("$c is crosslisted as $x")
            return temp.substitute({'c':database_answer["code"], 'x':database_answer["xlist"]})
        else:
            temp = Template("There are no crosslistings for $c")
            return temp.substitute({'c': database_answer["code"]})
    if isinstance(database_answer,list) and "instructor" in database_answer[0]:
        # string = database_answer[0]["code"] + " is taught by "
        # for r in database_answer:
        #     string += r["instructor"] + " "
        # return string
        from queryTables import compressList
        database_answer = compressList(database_answer)
        temp = Template("$c Duration $d is taught by $i")
        if database_answer["instructor"] == '':
            return "There are no listed instructors for this course"
        return temp.substitute({'c':database_answer["code"], 'i':database_answer["instructor"], 'd':database_answer["duration"]})
    if isinstance(database_answer,list) and "time" in database_answer[0]:
        string = ''
        temp = Template("$c Duration $du is at $t on $d")
        temp2 = Template("$c $f $fn Duration $du is at $t on $d")
        for r in database_answer:
            if not r["time"] == '':
                if "formatNum" in r:
                    string += temp2.substitute({'c':r["code"], 't':r["time"], 'd':r["days"], 'f':r["format"], 'fn':r["formatNum"], 'du':r["duration"]}) + '\n'
                else:
                    string += temp.substitute({'c':r["code"], 't':r["time"], 'd':r["days"], 'du':r["duration"]}) + '\n'
        return string
    
        # temp = Template("$c is at $t on $d")
        # return temp.substitute({'c':database_answer["code"], 't':database_answer["time"], 'd':database_answer["days"]})
    if isinstance(database_answer,list) and "location" in database_answer[0]:
        string = ''
        temp = Template("$c Duration $du is in room $l on $d")
        temp2 = Template("$c $f $fn Duration $du is in room $l on $d")
        for r in database_answer:
            # if not r["location"] == '':
            if "formatNum" in r:
                string += temp2.substitute({'c':r["code"], 'l':r["location"], 'd':r["days"], 'f':r["format"], 'fn':r["formatNum"], 'du':r["duration"]}) + '\n'
            else:
                string += temp.substitute({'c':r["code"], 'l':r["location"], 'd':r["days"], 'du':r["duration"]}) + '\n'
        print(string)
        return string
        # return temp.substitute({'c':database_answer["code"], 'l':database_answer["location"]})
    # response for prereqs (not great for single course prereqs or multi part questions?)
    if "prereq" in database_answer: 
        if database_answer["prereq"] != "": 
            temp = Template("The prerequisites for $c are $p" )
            return temp.substitute({'c': database_answer["code"], 'p':database_answer["prereq"]})
        else: 
            temp = Template("There are no prerequisites for $c")
            return temp.substitute({'c': database_answer["code"]})
    if "programName" in database_answer:
        temp = Template("You can find the information about this program by following this link $c")
        return temp.substitute({'c':database_answer["link"]})
    return None