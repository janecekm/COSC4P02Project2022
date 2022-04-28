from brockMatcher import getLink
import botNLP
import brockMatcher
def getQueries(question):
    matches, doc = botNLP.extractKeywords(question)
    return getLink(matches)

def testing_get_link_general():
    assert "https://brocku.ca/" in getQueries("what is prereq?")

def testing_get_link_exam():
    assert "https://brocku.ca/guides-and-timetables/exams/#more-exam-info" in getQueries("exam")

def testing_get_link_timetable():
    assert "https://brocku.ca/" in getQueries("COSC 1P02")
    assert "https://brocku.ca/" in getQueries("lab")

def testing_get_link_default_blank(): #blank query breaks really bad
    assert "https://brocku.ca/" in getQueries("")

def testing_get_link_default_garbage():
    assert "https://brocku.ca/" in getQueries("tauiwehiwuaegawugu")

def testing_get_link_advisor():
    assert "https://brocku.ca/academic-advising/find-your-advisor/" in getQueries("advisor")

def testing_get_link_tuition():
    assert "https://brocku.ca/safa/tuition-and-fees/overview/" in getQueries("tuition")
    assert "https://brocku.ca/safa/tuition-and-fees/overview/" in getQueries("cost")

def testing_get_link_covid():
    assert "https://brocku.ca/coronavirus/" in getQueries("coronavirus")
    assert "https://brocku.ca/coronavirus/" in getQueries("covid19")
    assert "https://brocku.ca/coronavirus/" in getQueries("quarantine")

def testing_get_link_food():
    assert "https://brocku.ca/dining-services/dining-on-campus/locations-on-campus-and-hours-of-operation/" in getQueries("food")
    assert "https://brocku.ca/dining-services/dining-on-campus/locations-on-campus-and-hours-of-operation/" in getQueries("eat")
    assert "https://brocku.ca/dining-services/dining-on-campus/locations-on-campus-and-hours-of-operation/" in getQueries("meal")

def testing_get_link_registration():
    assert "https://discover.brocku.ca/registration/" in getQueries("register")
    assert "https://discover.brocku.ca/registration/" in getQueries("registration")
    assert "https://discover.brocku.ca/registration/" in getQueries("choose my classes")

def testing_get_link_transit():
    assert "https://transitapp.com/region/niagara-region" in getQueries("travel")
    assert "https://transitapp.com/region/niagara-region" in getQueries("transit") #FAIL
    assert "https://transitapp.com/region/niagara-region" in getQueries("transportation")
    assert "https://transitapp.com/region/niagara-region" in getQueries("bus")

def testing_get_directory():
    assert "https://brocku.ca/directory/" in getQueries("contact")
    assert "https://brocku.ca/directory/" in getQueries("call")
    assert "https://brocku.ca/directory/" in getQueries("email")

def testing_get_store():
    assert "https://campusstore.brocku.ca/" in getQueries("store")
    assert "https://campusstore.brocku.ca/" in getQueries("textbook")