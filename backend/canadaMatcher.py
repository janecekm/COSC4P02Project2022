from spacy.tokens import Span
import os
from botNLP import nlp
from botNLP import matcher
from botNLP import phrase_matcher 

def filepath():
    if os.path.basename(os.getcwd()) == "backend":# we are in COSC4p02Project2022/backend
        return "./nlp-resources/"
    else:# we are in cosc4p02Project2022
        return "./backend/nlp-resources/"

###################################
sports = []
with open(filepath()+"sports-list.txt", encoding="utf-8") as f: 
    for line in f: 
        sports.append(line.strip())
    patterns = list(nlp.pipe(sports))
    phrase_matcher.add("sport", patterns)

venue = []
with open(filepath()+"venue-list.txt",encoding="utf-8") as t:
    for line in t:
        venue.append(line.strip())
    patterns = list(nlp.pipe(venue))
    phrase_matcher.add("venue",patterns)

muni = []
with open(filepath()+"town-list.txt",encoding="utf-8") as t:
    for line in t:
        muni.append(line.strip())
    patterns = list(nlp.pipe(muni))
    phrase_matcher.add("municipality",patterns)

###################################
# This section defines all the patterns for the Matcher

if not Span.has_extension("prio"): 
    Span.set_extension("prio", default=100)

def assignPriority(matcher, doc, i, matches): 
    match_id, start, end = matches[i]
    if match_id == nlp.vocab.strings["openerGreet"]\
        or match_id == nlp.vocab.strings["question"]:
        doc[start:end]._.prio = 3
    # elif match_id == nlp.vocab.strings["code"] \
    #     or match_id == nlp.vocab.strings["format"] \
    #     or match_id == nlp.vocab.strings["buildingCode"] :
    #     doc[start:end]._.prio = 2
    # elif match_id == nlp.vocab.strings["description"]: 
    #     doc[start:end]._.prio = 1
    else: # every other question term is more specific so it is highest prio
        doc[start:end]._.prio = 0

openerMatch = [{"LOWER": {"IN": ['hello','hi','hey','howdy','yo','sup','hiya','heyo']}}]
matcher.add("openerGreet", [openerMatch], on_match=assignPriority)

# location, what building, what venue, where 
location = [[{'LOWER':'location'}],
            [{'LOWER':'what'}, {'LOWER':'building'}], 
            [{'LOWER':'what'}, {'LOWER':'venue'}], 
            [{'LOWER': 'where'}]]
matcher.add("location", location, on_match=assignPriority)

# when is, when are, what time, what time is
when = [[{'LOWER': 'when'},
         {'LEMMA': 'be', "OP": "?"}],
        [{'LOWER': 'what'},
         {'LOWER': 'time'},
         {'LEMMA': 'be', "OP": "?"}]]
matcher.add("time", when, greedy="LONGEST", on_match=assignPriority)

# which sports are happening at venue?
# which sports are happening in town? 
# this is a rudimentary approach 
which = [[{'LOWER': 'which'}, 
         {'LEMMA': 'sport'}]]
matcher.add("which_sport", which, greedy="LONGEST")

# is sport at venue?

# we will need to add an appropriate links table here, similar to the one in brockMatcher
links = {
    "hi":"bye"
}
# we will also need to implement a "getLink(keywords)"

def getLink(matchedKeys):
    '''
    A method for if the info was not found in the database
    Args: 
        matchedKeys: the list of matches produced from extractKeywords 
                     [(match_id, start, end)]
                      match_id is a hashed value representing the type of match 
                      start is the start index of the matched span (set of tokens)
                      end is the end index of the matched span (set of tokens)
    Return: 
        returns a string to output as a response
    '''
    matches = []
    for match_id, start, end in matchedKeys:
        print(nlp.vocab.strings[match_id])
        matches.append(nlp.vocab.strings[match_id])
    if "openerGreet" in matches:
        return "Hello there"
    return links["hi"]

# dictionary updates: fonthill -> foothills, NOTL -> not 


