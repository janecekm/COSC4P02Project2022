import botNLP

def testing_invalid_input_ProcessQ():
    assert botNLP.processQ('raietweiaweeiiwnaeiugwe')['message'] == "I am not quite sure what you're asking. Could you rephrase that?"