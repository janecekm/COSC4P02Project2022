from concurrent.futures import process
from urllib import response
import spacy
from spacy.matcher import PhraseMatcher
import pkg_resources #resource for symspellpy
from spacy.matcher import Matcher
from symspellpy import SymSpell, Verbosity
from string import Template
import json
from spacy.tokens import Span
import os 
import platform

if os.path.basename(os.getcwd()) == "backend" and platform.system()=="Windows": 
    path = ".\\nlp-resources\\"
elif os.path.basename(os.getcwd()) == "COSC4P02Project2022" and platform.system()=="Windows": 
    path = ".\\backend\\nlp-resources\\"
elif os.path.basename(os.getcwd()) == "backend" and platform.system()=="Linux": 
    path = "./nlp-resources/"
else: 
    path = "./backend/nlp-resources/"

# load spacy
nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

###################################
# This section sets up the PhraseMatcher
# Currently the PhraseMatcher is used to extract only building codes
buildings = []
with open(path+"buildingCodesClean.txt", encoding="utf8") as f: 
    for line in f:
        buildings.append(json.loads(line)["buildingCode"])
patterns = list(nlp.pipe(buildings))
phrase_matcher.add("buildingCode", patterns)

###################################
# This section defines all the patterns for the Matcher

if not Span.has_extension("prio"): 
    Span.set_extension("prio", default=100)

def assignPriority(matcher, doc, i, matches): 
    match_id, start, end = matches[i]
    if match_id == nlp.vocab.strings["openerGreet"]\
        or match_id == nlp.vocab.strings["question"]:
        doc[start:end]._.prio = 3
    elif match_id == nlp.vocab.strings["code"] \
        or match_id == nlp.vocab.strings["course component"] \
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
            {'LOWER': 'professor'}]]
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

# generally the descriptions
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

# course components -- offering table
courseComp = [{'LEMMA': {"IN": ['sem', 'seminar', 'lab', 'tut', 'tutorial', 'lec', 'lecture', 'sec', 'section']}},
           {'LIKE_NUM': True, 'OP': '?'}]
matcher.add("course component", [courseComp], greedy="LONGEST", on_match=assignPriority)

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


admission = [[{'LEMMA':'apply'}], 
            [{'LEMMA':'admit'}], [{'LEMMA':'addmission'}] ]
matcher.add("admission", admission, on_match=assignPriority)


# store
store = [[{'LOWER':'store'}], [{'LEMMA':'textbook'}], [{'LEMMA':'booklist'}]]
matcher.add("store", store, on_match=assignPriority)
# end of Matcher pattern defintions

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = "backend\\nlp-resources\\frequency_dictionary_en_82_765.txt"
# term_index is the column of the term and count_index is the
# column of the term frequency
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
#sym_spell.create_dictionary_entry("cosc 1p02",50)
#play with words, adjust values accordingly. look into saving updated dictionary
# sym_spell.create_dictionary_entry("is",8569404971)
###########################################################
# links for when nothing is returned from the database
links = {
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
    # to be accomodated for:
    "programs" : "https://discover.brocku.ca/programs",
    "service_direct" : "https://brocku.ca/directory/a-z/",
    "news" : "https://brocku.ca/brock-news/", 
    "events" : "https://experiencebu.brocku.ca/",
    "facts" : "https://brocku.ca/about/brock-facts/"
}
###########################################################
def multiQuestionCheck(matches, doc):
    '''This method uses the matches and their corresponding priorities to see if the user has submitted multiple queries
    Args:
        matches: the list of matches returned from running the matcher on the document
        doc: the user text processed by the NLP pipeline (spaCy Doc object https://spacy.io/api/doc)
    Return:
        returns true if there is likely multiple questions, otherwise false
    '''
    labels = []

    for match_id, start, end in matches: 
        labels.append(nlp.vocab.strings[match_id])
    
    if labels.count('question') > 1:
        return False

    return True


def spellcheck(question, matches, doc): 
    '''This method performs a spellcheck on the question submitted by the user, after existing matches have been removed
    Args: 
        question: the original question string from the user
        matches: the list of matches returned from running the matcher on the document
        doc: the spaCy Doc object (https://spacy.io/api/doc) returned after running the string through the NLP pipeline
    Return: 
        matches: the list of matches after spellcheck has been applied (and the matcher has been re-run on the document)
        doc: the new Doc object (https://spacy.io/api/doc), run on the corrected string 
    '''
    suggestions = sym_spell.lookup_compound(
                question.lower(), max_edit_distance=2, ignore_non_words=True, ignore_term_with_digits=True)
    merge = suggestions[0].term
    doc = nlp(merge)
    matches = matcher(doc)
    phrase_matches = phrase_matcher(doc)
    for match in phrase_matches: 
        matches.append(match)
    return matches, doc 

def extractKeywords(question): 
    '''This method runs the matcher to extract key information from the query and add match labels
    Args:
        question: the string text to extract info from 
    Return: 
        matches: a list of matches where each is a tuple containing the match_id as a hash, and the indices of the start and end tokens
            [(match_id, start, end)]
            match_id is a hashed value representing the type of match 
            start is the start index of the matched span (set of tokens)
            end is the end index of the matched span (set of tokens)
        doc: the user input, processed by the NLP pipeline (output as a spaCy Doc object https://spacy.io/api/doc)
    '''
    doc = nlp(question)
    matches = matcher(doc)
    # get the phrase_matches and add them to the match list
    phrase_matches = phrase_matcher(doc) 
    for match in phrase_matches: 
        matches.append(match)
    print("Prior to correction:", doc.text)
    matches, doc = spellcheck(question, matches, doc)
    print("Post correction:", doc.text)
    return matches, doc

def processKeywords(matches, doc):
    '''Processes the extracted keyword matches into a format to give to the database 
    Args:
        matches: the list of matches
            [(match_id, start, end)]
            match_id is a hashed value representing the type of match 
            start is the start index of the matched span (set of tokens)
            end is the end index of the matched span (set of tokens)
        doc: the user text processed by the NLP pipeline (spaCy Doc object https://spacy.io/api/doc)
    Return: 
        a list of tuples containing the string version of the match_id and the matched text [(match_id_, match_text)]
    '''
    processedMatches = {}
    high_prio = False
    for match_id, start, end in matches: 
        match_label = nlp.vocab.strings[match_id]
        match_text = doc[start:end]
        match_text = match_text.text
        if not match_label == 'course component' and not match_label == 'question':
            processedMatches[match_label] = match_text
            if match_text._.prio == 0: 
                high_prio = True
            print("Match:", match_label, "\tMatch priority:", doc[start:end]._.prio)
        elif match_label == 'course component':
            comp = ''
            num = ''
            barred = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            
            for i in range(len(match_text)):
                if match_text[i] in barred:
                    num += match_text[i]
                elif not i == " ":
                    comp += match_text[i]
            processedMatches['format'] = comp.strip()
            processedMatches['format num'] = num
            
    # use the NER to extract the people names from document
    for ent in doc.ents:
        if (ent.label_ == "PERSON"):
            processedMatches["person"] = ent.text 
    if "description" in processedMatches.keys() and high_prio: 
        processedMatches.pop("description")
    return processedMatches

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
    temp = Template("I'm sorry, I wasn't able to find what you were looking for. However, you might be able to find more information at: $x")
    # for queries that we will exclusively be giving links to 
    temp2 = Template("Information regarding $y can be found at: $x")

    matches = []
    for match_id, start, end in matchedKeys:
        print(nlp.vocab.strings[match_id])
        matches.append(nlp.vocab.strings[match_id])
    if "prereqs" in matches:
        return temp.substitute({'x': links["prereqs"]})
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
    elif "course component" in matches or "course code" in matches:
        return temp.substitute({'x': links["timetable"]})
    elif "tuition" in matches:
        return temp2.substitute({'y' : "tuition", 'x': links["tuition"]})
    elif "openerGreet" in matches:
        return "What can I help you with today?"
    else:
        return temp.substitute({'x': links["brock"]})

def formResponse(database_answer, keys):
    '''A method to form a very simple response 
    Args: 
        matchedKeys: the list of match info as a result of processing
    Return: 
        returns a string to output as a response
    '''
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
    if "instructor" in database_answer:
        temp = Template("$c is taught by $i")
        return temp.substitute({'c':database_answer["code"], 'i':database_answer["instructor"]})
    if "time" in database_answer:
        temp = Template("$c is at $t on $d")
        return temp.substitute({'c':database_answer["code"], 't':database_answer["time"], 'd':database_answer["days"]})
    if "location" in database_answer:
        temp = Template("$c is in room $l")
        return temp.substitute({'c':database_answer["code"], 'l':database_answer["location"]})
    # response for prereqs (not great for single course prereqs or multi part questions?)
    if "prereq" in database_answer: 
        if database_answer["prereq"] != "": 
            temp = Template("The prerequisites for $c are $p" )
            return temp.substitute({'c': database_answer["code"], 'p':database_answer["prereq"]})
        else: 
            temp = Template("There are no prerequisites for $c")
            return temp.substitute({'c': database_answer["code"]})
    if database_answer == 'more info required' or database_answer == 'im in danger' or database_answer == "placeholder return": 
        # if no response from database
        return getLink(keys)
    return ""


def processQ(question):
    '''Main entry point to the NLP module. This is called by the server. 
    Args:
        question: the string of query text input by the user
    Return: 
        a response string to be output to the user
    '''
    matches, doc = extractKeywords(question)
    if multiQuestionCheck(matches, doc):
        processed = processKeywords(matches, doc)
        from queryTables import doQueries
        queryReturn = doQueries(processed)
        myString = ""
        if "hello" in question.lower():
            myString += "Hello! "
        myString += formResponse(queryReturn, matches)
        if (myString != "" and myString != None):    
            return {"message": myString}
        else:
            return {"message": "I am not quite sure what you're asking. Could you rephrase that?"}
    else:
        return {"message": "I'm sorry, that is a little too complicated for me. Please try rephrasing and limiting your questions to one at a time."}