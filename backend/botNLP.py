from urllib import response
import spacy
from spacy.matcher import PhraseMatcher
import pkg_resources #resource for symspellpy
from spacy.matcher import Matcher
from symspellpy import SymSpell, Verbosity
from string import Template
import json
import os

# load spacy
nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

###################################
# This section sets up the PhraseMatcher
# Currently the PhraseMatcher is used to extract only building codes
buildings = []
with open("backend\\nlp-resources\\buildingCodesClean.txt", encoding="utf8") as f: 
    for line in f:
        buildings.append(json.loads(line)["buildingCode"])
patterns = list(nlp.pipe(buildings))
phrase_matcher.add("buildingCode", patterns)

###################################
# This section defines all the patterns for the Matcher

# course codes -- course/offering/exam
courseCode = [[{'IS_ALPHA': True, 'LENGTH': 4},
               {'SHAPE': {'IN': ['dxdd', 'dXdd']}}],
             [{"SHAPE":  {'IN': ["xxxxdxdd", "Xxxxdxdd", "xXxxdxdd", "XXxxdxdd", "xxXxdxdd", "XxXxdxdd", "xXXxdxdd", "XXXxdxdd", "xxxXdxdd",
             "XxxXdxdd", "xXxXdxdd", "XXxXdxdd", "xxXXdxdd", "xXXXdxdd", "XXXXdxdd", "xxxxdXdd", "XxxxdXdd", "xXxxdXdd", "XXxxdXdd", "xxXxdXdd",
             "XxXxdXdd", "xXXxdXdd", "xxxXdXdd", "XxxXdXdd", "xXxXdXdd", "XXxXdXdd", "xxXXdXdd", "XxXXdXdd", "xXXXdXdd", "XXXXdXdd" ]}}]]
matcher.add("code", courseCode)

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
matcher.add("instructor", teaching)

# when is, when are, what time is
when = [[{'LOWER': 'when'},
         {'LEMMA': 'be', "OP": "?"}],
        [{'LOWER': 'what'},
         {'LOWER': 'time'},
         {'LEMMA': 'be'}]]
matcher.add("time", when, greedy="LONGEST")

# what are the prereq(uisites) -- course table
prerequisites = [[{'LOWER': 'what'},
                  {'OP': '?'},
                  {'OP': '?'},
                  {'LEMMA': 'prerequisite'}], 
                [{'LOWER': 'what'},
                  {'OP': '?'},
                  {'OP': '?'},
                  {'LEMMA': 'prereq'}]]
matcher.add("prereq", prerequisites)

# generally the descriptions
generalInfo = [ [{'LOWER':'tell'},{'LOWER':'me'},{'LOWER':'about'}], 
                [{'LOWER':'information'},{'LOWER':'on'}],
                [{'LOWER':'info'},{'LOWER':'on'}], 
                [{'LOWER': 'what'}, {'LOWER': 'is'}]]
matcher.add("description", generalInfo)

openerMatch = [{"LOWER": {"IN": ['hello','hi','hey','howdy','yo','sup','hiya','heyo']}}]
matcher.add("openerGreet", [openerMatch])

# don't have table
progQuestion = [{'LOWER':'the'},{'OP':'*'},{'LOWER':'program'}]
matcher.add("program question",[progQuestion])

# course components -- offering table
courseComp = [{'LEMMA': {"IN": ['sem', 'seminar', 'lab', 'tut', 'tutorial', 'lec', 'lecture', 'sec', 'section']}},
           {'LIKE_NUM': True, 'OP': '?'}]
matcher.add("course component", [courseComp], greedy="LONGEST")

# location -- offering or exam
location = [[{'LOWER':'location'}],
            [{'LOWER':'what'}, {'LOWER':'building'}], 
            [{'LOWER': 'where'}]]
matcher.add("location", location)

# exam table
exam = [{'LEMMA':'exam'}]
matcher.add("exam", [exam])

reqQuestion = [{'LOWER':'the'},{'LOWER':'program','OP':'?'},{'LOWER':'requirements'},{'LOWER':'for'}]

matcher.add("requirement question",[reqQuestion])

# advisor table
advisor = [{'LEMMA':'advisor'}]
matcher.add("advisor", [advisor])

# covid information
covid = [[{'LOWER':'covid'}],[{'LOWER':'covid19'}],[{'LOWER':'covid-19'}]
            ,[{'LOWER':'coronavirus'}],[{'LOWER':'quarantine'}],[{'LOWER':'lockdown'}]]
matcher.add("covid", covid)

# tuition
tuition = [[{'LEMMA':'cost'}],[{'LOWER':'tuition'}],[{'LEMMA':'price'}],[{'LOWER':'money'}],[{'LEMMA':'dollar'}],
            [{'LEMMA':'pay'}]]
matcher.add("tuition", tuition)

# food
food = [[{'LEMMA':'eat'}],[{'LOWER':'food'}],[{'LOWER':'breakfast'}],[{'LOWER':'lunch'}],[{'LOWER':'dinner'}],
            [{'LOWER':'meal'}],[{'LOWER':'mealplan'}],[{'LEMMA':'dining'}],[{'LEMMA':'snack'}]]
matcher.add("food", food)

# transportation, "How do I get to..."
transport = [[{'LEMMA':'travel'}],[{'LEMMA':'bus'}],[{'LEMMA':'transport'}],[{'LEMMA':'transportation'}],
                [{'LOWER': 'how'},
                  {'OP': '*'},
                  {'LEMMA': 'get'},
                  {'LEMMA': 'to'}]]
matcher.add("transport", transport)

# registration
register = [[{'LEMMA':'register'}],[{'LEMMA':'registration'}],
                [{'LOWER': 'choose'},{'OP': '?'},{'LEMMA': 'class'},],
                [{'LOWER': 'pick'},{'OP': '?'},{'LEMMA': 'class'},],
                [{'LOWER': 'choose'},{'OP': '?'},{'LEMMA': 'classes'},],
                [{'LOWER': 'pick'},{'OP': '?'},{'LEMMA': 'classes'},]]
matcher.add("register", register)

# directory
directory = [[{'LEMMA':'contact'}], [{'LOWER':'call'}], [{'LOWER':'phone'}], 
            [{'LOWER':'email'}], [{'LEMMA': 'speak'},{'LOWER': 'to'},]]
matcher.add("directory", directory)

# store
store = [[{'LOWER':'store'}], [{'LEMMA':'textbook'}], [{'LEMMA':'booklist'}]]
matcher.add("store", store)
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
    # to be accomodated for:
    "programs" : "https://discover.brocku.ca/programs",
    "service_direct" : "https://brocku.ca/directory/a-z/",
    "news" : "https://brocku.ca/brock-news/", 
    "events" : "https://experiencebu.brocku.ca/",
    "facts" : "https://brocku.ca/about/brock-facts/"
}
###########################################################


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
    for match_id, start, end in matches: 
        match_label = nlp.vocab.strings[match_id]
        match_text = doc[start:end]
        processedMatches[match_label] = match_text
    # use the NER to extract the people names from document
    for ent in doc.ents:
        if (ent.label_ == "PERSON"):
            processedMatches["person"] = ent.text 
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
    elif "store" in matches:
        return temp2.substitute({'y' : "the Brock Campus Store", 'x': links["store"]})
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
    elif "tuition" in matches:
        return temp2.substitute({'y' : "tuition", 'x': links["tuition"]})
    elif "advisor" in matches:
        return temp2.substitute({'y' : "academic advisors", 'x': links["acad_advisor"]})
    elif "exam" in matches:
        return temp.substitute({'x': links["exam"]})
    elif "course component" in matches or "course code" in matches:
        return temp.substitute({'x': links["timetable"]})
    else:
        return temp.substitute({'x': links["brock"]})

def formResponse(database_answer, keys):
    '''A method to form a very simple response 
    Args: 
        matchedKeys: the list of match info as a result of processing
    Return: 
        returns a string to output as a response
    '''
    # basic response for course descriptions (we should probably also be able to get course *names*)
    if "description" in database_answer: 
        temp = Template("The description for $c is:  $d")
        return temp.substitute({'c':database_answer["code"], 'd':database_answer["description"]})
    # response for prereqs (not great for single course prereqs or multi part questions?)
    if "prereq" in database_answer: 
        if database_answer["prereq"] != "": 
            temp = Template("The prerequisites for $c are $p" )
            return temp.substitute({'c': database_answer["code"], 'p':database_answer["prereq"]})
            
        else: 
            temp = Template("There are no prerequisites for $c")
            return temp.substitute({'c': database_answer["code"]})
    if "description" in database_answer:
        temp = Template("$c is all about $p")
        return temp.substitute({'c': database_answer["code"], 'p':database_answer["description"]})
    if "exam" in database_answer:
        temp = Template("$c has an exam on $d at $l")
        return temp.substitute({'c': database_answer["code"], 'd':database_answer["day"], 'l':database_answer["location"]})
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
    processed = processKeywords(matches, doc)
    from queryTables import doQueries
    queryReturn = doQueries(processed)
    print(queryReturn)
    myString = formResponse(queryReturn, matches)
    print(myString)
    if (myString != "" and myString != None):    
        return {"message": myString}
    else:
         return {"message": "I am not quite sure what you're asking. Could you rephrase that?"}