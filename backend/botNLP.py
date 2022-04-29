from symspellpy import SymSpell, Verbosity
import os
import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
# load spaCy + create Matcher and PhraseMatcher objects
nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
#setting up path for various nlp-resources such as autocorrect dictionary
localflag = 10
def filepath():
    if os.path.basename(os.getcwd()) =="backend":# we are in COSC4p02Project2022/backend
        return "./nlp-resources/"
    elif os.path.basename(os.getcwd())=="COSC4P02Project2022":# we are in cosc4p02Project2022
        return "./backend/nlp-resources/"
    else:
        return "./nlp-resources/"

###################################
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = filepath()+"frequency_dictionary_en_82_765.txt"
# term_index is the column of the term and count_index is the
# column of the term frequency
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
###########################################################

def multiQuestionCheck(matches, doc):
    '''Uses the matches and their corresponding priorities to see if the user has submitted multiple queries
    Args:
        matches: the list of matches returned from running the matcher on the document
        doc: the user text processed by the NLP pipeline (spaCy Doc object https://spacy.io/api/doc)
    Return:
        returns true if there is likely multiple questions, otherwise false
    '''
    labels = []

    for match_id, start, end in matches: 
        labels.append(nlp.vocab.strings[match_id])
    
    if labels.count('question') > 1:
        return False

    return True


def spellcheck(question): 
    '''Performs a spellcheck on the question submitted by the user
    Args: 
        question: the original question string from the user
    Return: 
        The spellcorrected user query as a string
    '''
    import re
    question = re.sub('[?|,|.|/|;|:|<|>|!|@|#|$|%|^|&|*|(|)|_|-|+|=|[|]|{|}|\"|\'|\\]','',question)
    questionPieces = question.split(" ")
    merge = ''
    for q in questionPieces:
        suggestion = sym_spell.lookup(q.lower(),Verbosity.TOP,max_edit_distance = 2,ignore_token= "[1234567890]")
        if suggestion:
            merge += suggestion[0].term + " "
        else:
            merge += q + " "
    return merge.strip()

def extractKeywords(question): 
    '''Runs the matcher to extract key information from the query and add match labels
    Args:
        question: the string text to extract info from 
    Return: 
        matches: a list of matches where each is a tuple containing the match_id as a hash, and the indices of the start and end tokens
            [(match_id, start, end)]
            match_id is a hashed value representing the type of match 
            start is the start index of the matched span (set of tokens)
            end is the end index of the matched span (set of tokens)
        doc: the user input, processed by the NLP pipeline (output as a spaCy Doc object https://spacy.io/api/doc)
    '''
    print("Prior to correction:", question)
    question = spellcheck(question)
    print("Post correction:", question)
    doc = nlp(question)
    matches = matcher(doc)
    # get the phrase_matches and add them to the match list
    phrase_matches = phrase_matcher(doc) 
    for match in phrase_matches: 
        matches.append(match)
    return matches, doc

def processKeywords(matches, doc):
    '''Processes the extracted keyword matches into a format to give to the database 
    Args:
        matches: the list of matches
            [(match_id, start, end)]
            match_id is a hashed value representing the type of match 
            start is the start index of the matched span (set of tokens)
            end is the end index of the matched span (set of tokens)
        doc: the user text processed by the NLP pipeline (spaCy Doc object https://spacy.io/api/doc)
    Return: 
        a list of tuples containing the string version of the match_id and the matched text [(match_id_, match_text)]
    '''
    processedMatches = {}
    high_prio = False
    for match_id, start, end in matches: 
        match_label = nlp.vocab.strings[match_id]
        match_text = doc[start:end]
        if not match_label == 'course component' and not match_label == 'question':
            if match_label == 'format':
                comp = ''
                num = ''
                barred = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                print(match_text.text)
                # for i in range(len(match_text)):
                #     if match_text[i].text in range(20):
                #         num += match_text[i].text
                #         print(num)
                #     elif not i == " ":
                #         comp += match_text[i].text
                temp = match_text.text.split(' ')
                processedMatches['format'] = temp[0]
                if len(temp) > 1:
                    processedMatches['formatNum'] = temp[1]
            else:
                processedMatches[match_label] = match_text.text
            if doc[start:end]._.prio == 0: 
                high_prio = True
            print("Match:", match_label, "\tMatch priority:", doc[start:end]._.prio)
        elif match_label == 'format':
            comp = ''
            num = ''
            barred = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            
            for i in range(len(match_text.text)):
                if match_text[i].text in barred:
                    num += match_text[i].text
                elif not i == " ":
                    comp += match_text[i].text
            processedMatches['format'] = comp.strip()
            processedMatches['formatNum'] = num
            
    # use the NER to extract the people names from document
    for ent in doc.ents:
        if (ent.label_ == "PERSON"):
            processedMatches["person"] = ent.text 
    if "description" in processedMatches.keys() and high_prio: 
        processedMatches.pop("description")
    return processedMatches

def processQ(question, flag=0):
    '''Main entry point to the NLP module. This is called by the server.
    Args:
        question: the string of query text input by the user
        flag: an integer indicating which chatbot is sending the request/which match patterns to use
              0 (default) indicates the Brock chat bot
              1 indicates Canada Games chat bot 
    Return: 
        a response string to be output to the user
    '''
    '''
    matcher: the matcher that is used for NLP pipeline, and this is build by the appropriate file, i.e. brockMatcher and canadaMatcher
    phrase_matcher: the phrase_matcher created by the appropriate file, i.e. brockMatcher or canadaMatcher
    formResponse: a method to form an appropriate response for the chatbot being used (specific to the keywords/data relevant to that chatbot)
    localflag: this is too indicate if brock match pattern has already been build or the canada games match pattern has been already build.
    '''
    global matcher, phrase_matcher, formResponse, localflag
    if flag == 0 and localflag!=flag: # we need to deconstruct the matcher each time to match the chat bot we are using
        from brockMatcher import matcher,phrase_matcher
        from brockMatcher import formResponse
        localflag = flag
    elif flag == 1 and localflag != flag:
        from canadaMatcher import matcher,phrase_matcher
        from canadaMatcher import formResponse # this function is abstracted so that the rules to define when we see a particular unknown case, we send them the link
        localflag = flag # this is done so that, if we build canada games matcher, we shouldn't be building it again
    matches, doc = extractKeywords(question)
    polite = False
    for match_id, start, end in matches:
        if "openerGreet".__contains__(nlp.vocab.strings[match_id]):
            polite = True
            break
    if multiQuestionCheck(matches, doc):
        processed = processKeywords(matches, doc)
        if flag == 0:
            from queryTables import doQueries
            queryReturn = doQueries(processed)
        elif flag == 1:
            from queryTables import cgQueries
            queryReturn = cgQueries(processed)
        myString = ""
        if polite:
            myString += "Hello! "
        myString += formResponse(queryReturn, matches)
        if (myString != "" and myString != None):    
            return {"message": myString}
        else:
            return {"message": "I am not quite sure what you're asking. Could you rephrase that?"}
    else:
        return {"message": "I'm sorry, that is a little too complicated for me. Please try rephrasing and limiting your questions to one at a time."}