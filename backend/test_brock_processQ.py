import botNLP
from brockMatcher import matcher,phrase_matcher

botNLP.matcher = matcher
botNLP.phrase_matcher = phrase_matcher
def askQuestion(question):
    return botNLP.processQ(question)["message"]

def testing_hello():
    assert "Hello" in askQuestion("Hello")
    assert "Hello" in askQuestion("Hello hello")

def test_prereqs():
    assert "COSC 1P02" in askQuestion("what are the prereqs for cosc 1p03")

def test_time():
    assert "19:00-21:00 on Monday" in askQuestion("when is cosc 1p03")

def test_sem_specific():
    assert "17:00-18:00" in askQuestion("when is clas 1p95 sem 9")
    assert "17:00-18:00" in askQuestion("when is seminar 9 for clas 1p95")

def test_random_input():
    assert "I'm sorry" in askQuestion("a;slkdf")

def test_links():
    assert "dining options" in askQuestion("where can I find food?")
    assert "Campus Store" in askQuestion("where can I find text books")
    assert "public transportation" in askQuestion("how do I get to brock campus")
    assert "registration process" in askQuestion("How do I register for courses?")
    assert "Mackenzie Chown Block" in askQuestion("where is mcj 205?")
    assert "Mackenzie Chown Block" in askQuestion("where is mcj205")
    assert "undergrad/" in askQuestion("what are the prereqs")

def test_rest_of_links():
    assert "exams" in askQuestion("where is my exam?")
    assert "washrooms" in askQuestion("where is the closest bathrooms")
    assert "COVID-19" in askQuestion("what are the latest covid procedures")

def test_where_class():
    assert "STH 204" in askQuestion("where is math 1p66")

def test_invalid_class():
    assert "brocku.ca" in askQuestion("where is cosc 4p44")

def test_component_grabber():
    assert "STH 204" in askQuestion("where is math 1p66 lec")
    assert "timetables/" in askQuestion("when is clas 1p97 lab")
    assert "11:00-13:00" in askQuestion("when is clas 1p97 lec")

def test_program_links():
    assert "undergraduate/computer-science/" in askQuestion("tell me more about Computer science program at brock")
    assert "undergraduate/economics/" in askQuestion("tell me more about econ")
    assert "undergraduate/computer-science/" in askQuestion("tell me about computer science at brock")