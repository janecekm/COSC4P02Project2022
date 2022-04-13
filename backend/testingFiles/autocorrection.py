import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import botNLP
##testing autocorrection
def correcting_english(question):
    nlp = spacy.load("en_core_web_md")
    matcher = Matcher(nlp.vocab)
    phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    doc = nlp(question)
    matches = matcher(doc)
    phrases_matched = phrase_matcher(doc)
    for match in phrases_matched:
        matches.append(match)
    return botNLP.spellcheck(question,matches,doc)

def testing_spelling_mistake():
    matches, docs = correcting_english("hello there")
    print(matches)
    print(docs)