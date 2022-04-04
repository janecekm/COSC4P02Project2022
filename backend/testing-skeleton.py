import botNLP

error_message = "I'm sorry, I wasn't able to find what you were looking for. However, you might be able to find more information at: https://brocku.ca/"
#botNLP.ProcessQ
def testing_invalid_input_ProcessQ():
    assert botNLP.processQ('raietweiaweeiiwnaeiugwe')['message'] == "I am not quite sure what you're asking. Could you rephrase that?"
def testing_valid_input_ProcessQ():
    assert 'COSC 1P02' in botNLP.processQ('What is the prereqs for COSC 1P03')['message']
def testing_valid_misspelled_input_ProcessQ():
    assert 'COSC 1P02' in botNLP.processQ('What aer the Prereq for COSC 1p03')['message']
def testing_valid_more_misspelled_input_ProcessQ():
    assert botNLP.processQ('Qjtat is jet prereq for COSC 1p03')['message'] == "I am not quite sure what you're asking. Could you rephrase that?"
def testing_misspelled_wat_input_ProcessQ():
    assert 'COSC 1P02' in botNLP.processQ('Wat is prereqs for COSC 1P03')['message'] 
def testing_attempt_SQL_injection1_ProcessQ():
    assert botNLP.processQ('What are the prereqs for *’-- 1P02')['message'] == error_message
def testing_attempt_SQL_injection2_ProcessQ():
    assert botNLP.processQ('What are the prereqs for /**/ *’--')['message'] == error_message
def testing_single_hello_processQ():
    assert botNLP.processQ('Hello Hello') == "Hello"

#botNLP.getLink
def testing_prereq_getLink():
    assert 'https://brocku.ca/webcal/undergrad/' in botNLP.getLink({'prereq'})
