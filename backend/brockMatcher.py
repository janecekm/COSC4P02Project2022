import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import os
import json
nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

def filepath():
    if os.path.basename(os.getcwd()) =="backend":#we are in COSC4p02Project2022/backend
        return "./nlp-resources/"
    else:#we are in cosc4p02Project2022
        return "./backend/nlp-resources/"

buildings = []
with open(filepath()+"buildingCodesClean.txt", encoding="utf8") as f: 
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

crosslist = [[{'LOWER': 'what'},
                  {'OP': '?'},
                  {'OP': '?'},
                  {'LEMMA': 'crosslist'}], 
                [{'LOWER': 'what'},
                  {'OP': '?'},
                  {'OP': '?'},
                  {'LEMMA': 'xlist'}]]
matcher.add("xlist", crosslist)

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
matcher.add("format", [courseComp], greedy="LONGEST")

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