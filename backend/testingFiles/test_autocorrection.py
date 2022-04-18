import botNLP

##testing autocorrection
def correcting_english(question):
    doc = botNLP.nlp(question)
    matches = botNLP.matcher(doc)
    phrases_matched = botNLP.phrase_matcher(doc)
    for match in phrases_matched:
        matches.append(match)
    return botNLP.spellcheck(question,matches,doc)[1].text

def testing_spelling_mistake():
    # matches, docs = correcting_english("waht there")
    assert correcting_english("waht there") == "what there"
    # matches, docs = correcting_english("helo there, hw is it going?")
    assert correcting_english("helo there, hw is it going?") == "hello there, how is it going"
    assert correcting_english("wht are prere for Math 4p61") == "what are prereqs for math 4p61"

def testing_course_spelling():
    assert correcting_english("what are prereqs for csc 1p02") == "what are prereqs for csc 1p02"
    assert correcting_english("what are the prerequistes for COSC 1p03") == "what are the prerequisites for cosc 1p03"