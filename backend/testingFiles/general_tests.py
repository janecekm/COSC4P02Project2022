from queryTables import doQueries
from numpy import extract
from py import process
import botNLP
import os

error_message_1 = "I'm sorry, I wasn't able to find what you were looking for. However, you might be able to find more information at: https://brocku.ca/"
error_message_2 = "I am not quite sure what you're asking. Could you rephrase that?"
#botNLP.ProcessQ
def testing_invalid_input_ProcessQ():
    assert (botNLP.processQ('raietweiaweeiiwnaeiugwe')['message'] == error_message_1) or (botNLP.processQ('raietweiaweeiiwnaeiugwe')['message'] == error_message_2)
def testing_valid_input_ProcessQ():
    assert 'COSC 1P02' in botNLP.processQ('What is the prereqs for COSC 1P03')['message']
def testing_valid_misspelled_input_ProcessQ():
    assert 'COSC 1P02' in botNLP.processQ('What aer the Prereq for COSC 1p03')['message']
def testing_valid_more_misspelled_input_ProcessQ():
    assert ("COSC 1P02" in botNLP.processQ('Qjtat is jet prereq for COSC 1p03')['message'])
def testing_misspelled_wat_input_ProcessQ():
    assert 'COSC 1P02' in botNLP.processQ('Wat is prereqs for COSC 1P03')['message'] 
def testing_attempt_SQL_injection1_ProcessQ():
    assert (botNLP.processQ('What are the prereqs for *’-- 1P02')['message'] == error_message_1) or (botNLP.processQ('What are the prereqs for *’-- 1P02')['message'] == error_message_2)
def testing_attempt_SQL_injection2_ProcessQ():
    assert (botNLP.processQ('What are the prereqs for /**/ *’--')['message'] == error_message_1) or (botNLP.processQ('What are the prereqs for /**/ *’--')['message'] == error_message_2) 
def testing_single_hello_processQ():
    assert botNLP.processQ('Hello Hello')['message']== "Hello! What can I help you with today?"

def testing_spacefor_course():
    assert 'MATH 1P66' in botNLP.processQ("what are prereq for math1p67")['message']

#botNLP.getLink 
#FAILED testingFiles/general_tests.py::testing_prereq_getLink - ValueError: not enough values to unpack (expected 3, got 1)
def testing_prereq_getLink():
    assert 'https://brocku.ca/webcal/undergrad/' in botNLP.getLink('prereq')

def filepath():
    if os.path.basename(os.getcwd()) =="backend":#we are in COSC4p02Project2022/backend
        return "./nlp-resources/"
    else:#we are in cosc4p02Project2022
        return "./backend/nlp-resources/"

def testing_filegrabber():
    assert open(filepath()+"buildingCodesClean.txt","r")
    os.chdir("..")
    assert open(filepath()+"buildingCodesClean.txt","r")