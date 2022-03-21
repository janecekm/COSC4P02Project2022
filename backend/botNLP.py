from urllib import response
import spacy
import pkg_resources #resource for symspellpy
from spacy.matcher import Matcher
from symspellpy import SymSpell, Verbosity
from string import Template
import re

# load spacy
nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)

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
progQuestion = [{'LOWER':'the'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'LOWER':'program'}]

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

# end of Matcher pattern defintions

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt"
)
# term_index is the column of the term and count_index is the
# column of the term frequency
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
#sym_spell.create_dictionary_entry("cosc 1p02",50)
#play with words, adjust values accordingly. look into saving updated dictionary
sym_spell.create_dictionary_entry("is",8569404971)

###########################################################
# links for when nothing is returned from the database
links = {
    "prereqs" : "https://brocku.ca/webcal/undergrad/",
    "exam" : "https://brocku.ca/guides-and-timetables/exams/#more-exam-info",
    "timetable" : "https://brocku.ca/guides-and-timetables/timetables/",
    "brock" : "https://brocku.ca/", 
    "directory":"https://brocku.ca/directory/", 
    "acad_advisor": "https://brocku.ca/academic-advising/find-your-advisor/"
}
###########################################################

def extractKeywords(question): 
    '''This method runs the matcher to extract key information from the query and add match labels
    Args:
        question: the string text to extract info from 
    Return: 
        matches: a list of matches where each is a tuple containing the match_id as a hash, and the indices of the start and end tokens
        doc: the user input, processed by the NLP pipeline
    '''
    doc = nlp(question)
    orig = question.split(" ")
    matches = matcher(doc)
    #autocorrection layer
    for match_id, start, end in matches:
        if (str(doc[start:end]).strip() in question):
            length = len(str(doc[start:end]).split(" "))
            string = " oodles " * length
            question = question.replace(str(doc[start:end]), string)
    question = question.replace("  "," ")
    suggestions = sym_spell.lookup_compound(
        question, max_edit_distance=2
    )
    fix = str(suggestions[0]).split(",")[0].split(" ")
    for i in range(len(orig)):
        if orig[i] != fix[i] and fix[i] != "oodles":
            orig[i] = fix[i]
    merge = " ".join(orig)
    doc = nlp(merge)
    matches = matcher(doc)
    #end of autocorrection

    return matches, doc

def processKeywords(matches, doc):
    '''Processes the extracted keyword matches into a format to give to the database 
    Args:
        matches: the list of matches
        doc: the user text processed by the NLP pipeline
    Return: 
        a list of tuples containing the string of the match_id and the matched text [(match_id_, match_text)]
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
        matchedKeys: the list of match info as a result of processing
    Return: 
        returns a string to output as a response
    '''
    temp = Template("I'm sorry, I wasn't able to find what you were looking for. However, you might be able to find more information at: $x")
    matches = []
    for match_id, start, end in matchedKeys:
        print(nlp.vocab.strings[match_id])
        matches.append(nlp.vocab.strings[match_id])
    if "prereqs" in matches:
        return temp.substitute({'x': links["prereqs"]})
    if "exam" in matches:
        return temp.substitute({'x': links["exam"]})
    if "course component" in matches or "course code" in matches:
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
    if database_answer == 'more info required' or database_answer == 'im in danger': 
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
    myString = formResponse(queryReturn, matches)
    if (myString != "" and myString != None):    
        return {"message": myString}
    else:
         return {"message": "I am not quite sure what you're asking. Could you rephrase that?"}