import botNLP

def testing_invalid_input_ProcessQ():
    assert botNLP.processQ('raietweiaweeiiwnaeiugwe')['message'] == "I am not quite sure what you're asking. Could you rephrase that?"
def testing_valid_input_ProcessQ():
    assert botNLP.processQ('What are the prereqs for COSC 1P03')['message'].contains("COSC 1P02")
