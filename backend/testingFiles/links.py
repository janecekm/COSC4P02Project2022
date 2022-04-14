import botNLP


def testing_get_link_general():
    print(botNLP.processQ("prereqs")['message'])
    assert "https://brocku.ca/webcal/undergrad/" in botNLP.processQ("prereqs")['message']

def testing_get_link_exam():
    assert "https://brocku.ca/guides-and-timetables/exams/#more-exam-info" in botNLP.processQ("exam")['message']

def testing_get_link_timetable():
    assert "https://brocku.ca/guides-and-timetables/timetables/" in botNLP.processQ("COSC 1P02")['message']
    assert "https://brocku.ca/guides-and-timetables/timetables/" in botNLP.processQ("lab")['message']

def testing_get_link_default_blank():
    assert "https://brocku.ca/" in botNLP.processQ("")['message']

def testing_get_link_default_garbage():
    assert "https://brocku.ca/" in botNLP.processQ("tauiwehiwuaegawugu")['message']

def testing_get_link_advisor():
    assert "https://brocku.ca/academic-advising/find-your-advisor/" in botNLP.processQ("advisor")['message']

def testing_get_link_tuition():
    assert "https://brocku.ca/safa/tuition-and-fees/overview/" in botNLP.processQ("tuition")['message']
    assert "https://brocku.ca/safa/tuition-and-fees/overview/" in botNLP.processQ("cost")['message']

def testing_get_link_covid():
    assert "https://brocku.ca/coronavirus/" in botNLP.processQ("coronavirus")['message']
    assert "https://brocku.ca/coronavirus/" in botNLP.processQ("covid19")['message']
    assert "https://brocku.ca/coronavirus/" in botNLP.processQ("quarantine")['message']

def testing_get_link_food():
    assert "https://brocku.ca/dining-services/dining-on-campus/locations-on-campus-and-hours-of-operation/" in botNLP.processQ("food")['message']
    assert "https://brocku.ca/dining-services/dining-on-campus/locations-on-campus-and-hours-of-operation/" in botNLP.processQ("eat")['message']
    assert "https://brocku.ca/dining-services/dining-on-campus/locations-on-campus-and-hours-of-operation/" in botNLP.processQ("meal")['message']

def testing_get_link_registration():
    assert "https://discover.brocku.ca/registration/" in botNLP.processQ("register")['message']
    assert "https://discover.brocku.ca/registration/" in botNLP.processQ("registration")['message']
    assert "https://discover.brocku.ca/registration/" in botNLP.processQ("choose my classes")['message']

def testing_get_link_transit():
    assert "https://transitapp.com/region/niagara-region" in botNLP.processQ("travel")['message']
    assert "https://transitapp.com/region/niagara-region" in botNLP.processQ("transit")['message']
    assert "https://transitapp.com/region/niagara-region" in botNLP.processQ("transportation")['message']
    assert "https://transitapp.com/region/niagara-region" in botNLP.processQ("bus")['message']

def testing_get_directory():
    assert "https://brocku.ca/directory/" in botNLP.processQ("contact")['message']
    assert "https://brocku.ca/directory/" in botNLP.processQ("call")['message']
    assert "https://brocku.ca/directory/" in botNLP.processQ("email")['message']

def testing_get_store():
    assert "https://campusstore.brocku.ca/" in botNLP.processQ("store")['message']
    assert "https://campusstore.brocku.ca/" in botNLP.processQ("textbook")['message']
    assert "https://campusstore.brocku.ca/" in botNLP.processQ("booklist")['message']