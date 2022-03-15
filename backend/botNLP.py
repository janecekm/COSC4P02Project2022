import spacy
from spacy.matcher import Matcher
from string import Template

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
matcher.add("course code", courseCode)

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
matcher.add("prereqs", prerequisites)

# generally the descriptions
generalInfo = [ [{'LOWER':'tell'},{'LOWER':'me'},{'LOWER':'about'}], 
                [{'LOWER':'information'},{'LOWER':'on'}],
                [{'LOWER':'info'},{'LOWER':'on'}], 
                [{'LOWER': 'what'}, {'LOWER': 'is'}]]

matcher.add("general question", generalInfo)

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
    matches = matcher(doc)
    return matches, doc

def processKeywords(matches, doc):
    '''Processes the extracted keyword matches into a format to give to the database 
    Args:
        matches: the list of matches
        doc: the user text processed by the NLP pipeline
    Return: 
        a list of tuples containing the string of the match_id and the matched text [(match_id_, match_text)]
    '''
    processedMatches = []
    for match_id, start, end in matches: 
        match_label = nlp.vocab.strings[match_id]
        match_text = doc[start:end]
        processedMatches.append((match_label, match_text))
    # use the NER to extract the people names from document
    for ent in doc.ents:
        if (ent.label_ == "PERSON"):
            processedMatches.append(("person", ent.text))  
    return processedMatches

def formResponse(matchedKeys):
    '''A method to form a very simple response 
    Args: 
        matchedKeys: the list of match info as a result of processing
    Return: 
        returns a string to output as a response
    '''
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
    '''Main entry point to the NLP module. This is called by the server. 
    Args:
        question: the string of query text input by the user
    Return: 
        a response string to be output to the user
    '''
    matches, doc = extractKeywords(question)
    processed = processKeywords(matches, doc)
    myString = formResponse(matches)
    if (myString != "" and myString != None):    
        return {"message": myString}
    else:
         return {"message": "I am not quite sure what you're asking. Could you rephrase that?"}