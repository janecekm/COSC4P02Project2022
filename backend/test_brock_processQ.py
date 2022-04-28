import botNLP

def askQuestion(question):
    return botNLP.processQ(question)["message"]

def testing_hello():
    assert "Hello" in askQuestion("Hello")

def test_prereqs():
    assert "COSC 1P02" in askQuestion("what are the prereqs for cosc 1p03")