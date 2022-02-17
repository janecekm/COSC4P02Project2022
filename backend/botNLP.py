import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)

# course codes
courseCaps = [{'IS_ALPHA': True, 'LENGTH': 4},
           {'SHAPE': 'dXdd'}]
courseLower = [{'IS_ALPHA': True, 'LENGTH': 4},
           {'SHAPE': 'dxdd'}]
matcher.add("CourseCode", [courseCaps, courseLower])

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
matcher.add("QInstructor", [teaching, instructor, professor])

# when is, when are, what time is
when = [{'LOWER': 'when'},
           {'LEMMA': 'be'}]
whatTime = [{'LOWER': 'what'},
           {'LOWER': 'time'},
           {'LEMMA': 'be'}]
matcher.add("QTime", [when, whatTime])

# what are the prereq(uisites)
prerequisites = [{'LOWER': 'what'},
           {'OP': '?'},
           {'OP': '?'},
           {'LEMMA': 'prerequisites'}]
prereqs = [{'LOWER': 'what'},
           {'OP': '?'},
           {'OP': '?'},
           {'LEMMA': 'prereqs'}]
matcher.add("QPrereqs", [prerequisites, prereqs])

generalTell = [{'LOWER':'tell'},{'LOWER':'me'},{'LOWER':'about'}]
generalInfoOn = [{'LOWER':'information'},{'LOWER':'on'}]
generalInfoOn2 = [{'LOWER':'info'},{'LOWER':'on'}]

matcher.add("General Question",[generalTell, generalInfoOn, generalInfoOn2])

openerGreeting = ['hello','hi','hey','howdy','yo','sup','hiya','heyo']
openerMatch = []
for opener in openerGreeting:
  openerMatch.append([{'LOWER':opener}])

matcher.add("openerGreet",openerMatch)

progQuestion = [{'LOWER':'the'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'OP':'?'},{'LOWER':'program'}]

matcher.add("Program Question",[progQuestion])

# course components
sem = [{'LOWER': 'sem'},
           {'LIKE_NUM': True, 'OP': '?'}]
seminar = [{'LEMMA': 'seminar'},
           {'LIKE_NUM': True, 'OP': '?'}]
lab = [{'LEMMA': 'lab'},
           {'LIKE_NUM': True, 'OP': '?'}]
tutorial = [{'LEMMA': 'tutorial'},
           {'LIKE_NUM': True, 'OP': '?'}]
tut = [{'LEMMA': 'tut'},
           {'LIKE_NUM': True, 'OP': '?'}]
lecture = [{'LEMMA': 'lecture'},
           {'LIKE_NUM': True, 'OP': '?'}]
lec = [{'LEMMA': 'lec'},
           {'LIKE_NUM': True, 'OP': '?'}]

matcher.add("CourseComponent", [sem, seminar, lab, tutorial, tut, lecture, lec])

# location
where = [{'LOWER': 'where'}]
whatBuilding = [{'LOWER':'what'}, {'LOWER':'building'}]
location = [{'LOWER':'location'}]

matcher.add("QLocation", [where, whatBuilding, location])

# exam
exam = [{'LEMMA':'exam'}]
matcher.add("QExam", [exam])

# exists
does = [{'LOWER':'does'}]
matcher.add("QExists", [does])


reqQuestion = [{'LOWER':'the'},{'LOWER':'program','OP':'?'},{'LOWER':'requirements'},{'LOWER':'for'}]

matcher.add("Requirement Question",[reqQuestion])

def processQ(question):
    doc = nlp(question)
    matches = matcher(doc)
    myString = ""
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # get string rep
        span = doc[start:end]  # matched span
        myString = myString + str(string_id) + " " + str(start) + " " + str(end) + " " + str(span.text) + " "
    if (myString != ""):
        print(myString)
        print(type(myString))
        return {"message": myString}
    else:
        return {"message": "does not compute"}