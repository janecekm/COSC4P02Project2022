from spacy.tokens import Span
from botNLP import nlp
from spacy.matcher import Matcher,PhraseMatcher
from string import Template

matcher = Matcher(nlp.vocab)
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER") # case insensitive phrase matching

from botNLP import filepath

###################################
# PhraseMatcher initialization
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
    '''Assigns priorities to matched spans based on component importantance. 
    Lower prio values correspond to higher priorities. 
    '''
    match_id, start, end = matches[i]
    if match_id == nlp.vocab.strings["openerGreet"]\
        or match_id == nlp.vocab.strings["question"]:
        doc[start:end]._.prio = 3
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
which = [[{'LOWER': 'which'}, 
         {'LEMMA': 'sport'}]]
matcher.add("which_sport", which, greedy="LONGEST")

# tickets
ticket = [[{'LEMMA':'ticket'}]]
matcher.add("ticket", ticket, on_match=assignPriority)

# volunteer
volunteer = [[{'LEMMA':'volunteer'}]]
matcher.add("volunteer", volunteer, on_match=assignPriority)

# transportation, "How do I get to..."
transport = [[{'LEMMA':'transit'}],[{'LEMMA':'travel'}],[{'LEMMA':'bus'}],[{'LEMMA':'transport'}],[{'LEMMA':'transportation'}],
                [{'LOWER': 'how'},
                  {'OP': '*'},
                  {'LEMMA': 'get'},
                  {'LEMMA': 'to'}]]
matcher.add("transport", transport, on_match=assignPriority)
####################################

# link table for questions that should give link responses
links = {
    "transit" : "https://transitapp.com/region/niagara-region",
    "schedule" : "https://cg2022.gems.pro/Result/Calendar.aspx",
    "location" : "https://niagara2022games.ca/sports/", 
    "ticket" : "https://niagara2022games.ca/tickets/", 
    "default" : "https://www.canadagames.ca/", 
    "volunteer" : "https://www.canadagames.ca/about/faq?tab=volunteers#faq"
}

# getLink method that utilizes the appropriate link table and key values for Canada Games
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
    temp = Template("I'm sorry, I wasn't able to find what you were looking for. However, you might be able to find more information at: $x")
    # for queries that we will exclusively be giving links to 
    temp2 = Template("Information regarding $y can be found at: $x")

    matches = []
    for match_id, start, end in matchedKeys:
        matches.append(nlp.vocab.strings[match_id])

    if "ticket" in matches:
        return temp2.substitute({'y':"tickets",'x':links["ticket"]})
    elif "volunteer" in matches:
        return temp.substitute({'x': links["volunteer"]})
    elif "location" in matches:
        return temp.substitute({'x': links["location"]})
    elif "time" in matches:
        return temp.substitute({'x': links["schedule"]})
    elif "transport" in matches:
        return temp2.substitute({'y' : "local public transportation", 'x': links["transit"]})
    else: 
        return temp.substitute({'x': links["default"]})

# this function needs to be filled out for the chatbot to know how to form response.
def formResponse(database_answer, keys):
    '''A method to form a response 
    Args: 
        database_answer: response from the database, will be of type dictionary, list or None if no response from database
        keys: the list of match info as a result of processing
    Return: 
        returns a string to output as a response
    '''
    if not database_answer:
        return getLink(keys)
    if isinstance(database_answer,list) and "location" in database_answer[0]:
        from queryTables import compressList
        database_answer = compressList(database_answer)
        temp = Template("$s is hosted at $v")
        return temp.substitute({'s':database_answer["sport"].capitalize(), 'v':database_answer["venue"]})
    if isinstance(database_answer,list) and "time" in database_answer[0]:
        string = ''
        temp = Template("$g $s is at $t on $m $d at $v")
        for r in database_answer:
            string += temp.substitute({'s':r["sport"], 'm':r["month"], 'd':r["date"], 't':r["time"], 'g':r["gender"], 'v':r["venue"]}) + '\n'
        return string
    return None