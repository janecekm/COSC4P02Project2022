from symspellpy import SymSpell, Verbosity
from string import Template
import os
import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
#setting up path for various nlp-resources such as autocorrect dictionary
localflag = 10
def filepath():
    if os.path.basename(os.getcwd()) =="backend":#we are in COSC4p02Project2022/backend
        return "./nlp-resources/"
    else:#we are in cosc4p02Project2022
        return "./backend/nlp-resources/"

###################################
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = filepath()+"frequency_dictionary_en_82_765.txt"
# term_index is the column of the term and count_index is the
# column of the term frequency
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
#sym_spell.create_dictionary_entry("cosc 1p02",50)
#play with words, adjust values accordingly. look into saving updated dictionary
# sym_spell.create_dictionary_entry("is",8569404971)
###########################################################
# links for when nothing is returned from the database
###########################################################
def multiQuestionCheck(matches, doc):
    '''This method uses the matches and their corresponding priorities to see if the user has submitted multiple queries
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


def spellcheck(question, matches, doc): 
    '''This method performs a spellcheck on the question submitted by the user, after existing matches have been removed
    Args: 
        question: the original question string from the user
        matches: the list of matches returned from running the matcher on the document
        doc: the spaCy Doc object (https://spacy.io/api/doc) returned after running the string through the NLP pipeline
    Return: 
        matches: the list of matches after spellcheck has been applied (and the matcher has been re-run on the document)
        doc: the new Doc object (https://spacy.io/api/doc), run on the corrected string 
    '''
    questionPieces = question.split(" ")
    merge = ''
    for q in questionPieces:
        suggestion = sym_spell.lookup(q.lower(),Verbosity.TOP,max_edit_distance = 2,ignore_token= "[!@£#$%^&*();,.?:{}/|<>1234567890]")
        if suggestion:
            merge += suggestion[0].term + " "
        else:
            merge += q + " "
    doc = nlp(merge.strip())
    matches = matcher(doc)
    phrase_matches = phrase_matcher(doc)
    for match in phrase_matches: 
        matches.append(match)
    return matches, doc 

def extractKeywords(question): 
    '''This method runs the matcher to extract key information from the query and add match labels
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
    doc = nlp(question)
    matches = matcher(doc)
    # get the phrase_matches and add them to the match list
    phrase_matches = phrase_matcher(doc) 
    for match in phrase_matches: 
        matches.append(match)
    print("Prior to correction:", doc.text)
    matches, doc = spellcheck(question, matches, doc)
    print("Post correction:", doc.text)
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
        # match_text = match_text.text
        if not match_label == 'course component' and not match_label == 'question':
            processedMatches[match_label] = match_text
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
            processedMatches['format num'] = num
            
    # use the NER to extract the people names from document
    for ent in doc.ents:
        if (ent.label_ == "PERSON"):
            processedMatches["person"] = ent.text 
    if "description" in processedMatches.keys() and high_prio: 
        processedMatches.pop("description")
    return processedMatches



def formResponse(database_answer, keys):
    '''A method to form a very simple response 
    Args: 
        matchedKeys: the list of match info as a result of processing
    Return: 
        returns a string to output as a response
    '''
    if not database_answer:
        return ""
    if "buildingCode" in database_answer:
        temp = Template("$c is the building code for $n. For more details see $l.")
        return temp.substitute({'c':database_answer["buildingCode"], 'n':database_answer["name"], 'l':"https://brocku.ca/blogs/campus-map/"})
    if "exam" in database_answer:
        temp = Template("$c has an exam on $m $d at $t $l")
        return temp.substitute({'c': database_answer["code"], 'm':database_answer["month"], 'd':database_answer["dayNum"], 't':database_answer["time"], 'l':database_answer["location"]})
    # basic response for course descriptions
    if "description" in database_answer: 
        temp = Template("$c is $t and it's about $d")
        return temp.substitute({'c':database_answer["code"], 't':database_answer["title"], 'd':database_answer["description"]})
    if "xlist" in database_answer:
        if database_answer["xlist"] != "":
            temp = Template("$c is crosslisted as $x")
            return temp.substitute({'c':database_answer["code"], 'x':database_answer["xlist"]})
        else:
            temp = Template("There are no crosslistings for $c")
            return temp.substitute({'c': database_answer["code"]})
    if "instructor" in database_answer[0]:
        # string = database_answer[0]["code"] + " is taught by "
        # for r in database_answer:
        #     string += r["instructor"] + " "
        # return string
        from queryTables import compressList
        database_answer = compressList(database_answer)
        temp = Template("$c is taught by $i")
        if database_answer["instructor"] == '':
            return "There are no listed instructors for this course"
        return temp.substitute({'c':database_answer["code"], 'i':database_answer["instructor"]})
    if "time" in database_answer[0]:
        string = ''
        temp = Template("$c is at $t on $d")
        for r in database_answer:
            if not r["time"] == '':
                string += temp.substitute({'c':r["code"], 't':r["time"], 'd':r["days"]})
        return string
    
        # temp = Template("$c is at $t on $d")
        # return temp.substitute({'c':database_answer["code"], 't':database_answer["time"], 'd':database_answer["days"]})
    if "location" in database_answer:
        temp = Template("$c is in room $l")
        return temp.substitute({'c':database_answer["code"], 'l':database_answer["location"]})
    # response for prereqs (not great for single course prereqs or multi part questions?)
    if "prereq" in database_answer: 
        if database_answer["prereq"] != "": 
            temp = Template("The prerequisites for $c are $p" )
            return temp.substitute({'c': database_answer["code"], 'p':database_answer["prereq"]})
        else: 
            temp = Template("There are no prerequisites for $c")
            return temp.substitute({'c': database_answer["code"]})
    if database_answer == 'more info required' or database_answer == 'im in danger' or database_answer == "placeholder return": 
        # if no response from database
        return getLink(keys)
    return ""

def processQ(question, flag=0):
    '''Main entry point to the NLP module. This is called by the server.
    Args:
        question: the string of query text input by the user
        flag: an integer indicating which chatbot is sending the request/which match patterns to use
              0 (default) indicates the Brock chat bot
              1 indicates Canada Games chat bot 
              ** Note: this functionality is not yet completely implemented
    Return: 
        a response string to be output to the user
    '''
    '''
    matcher : the matcher that is used for NLP pipeline, and this is build by the appropriate file, i.e. brockMatcher and canadaMatcher
    phrase_matcher : the phrase_matcher created by the appropriate file, i.e. brockMatcher or canadaMatcher
    getLink : the rule set applied to the links that needs to be returned if a answer is not found.
    localflag : this is too indicate if brock match pattern has already been build or the canada games match pattern has been already build.
    '''
    global matcher, phrase_matcher, links, getLink, localflag
    if flag == 0 and localflag!=flag: # we need to deconstruct the matcher each time to match the chat bot we are using
        import brockMatcher
        from brockMatcher import getLink
        from brockMatcher import links
        localflag = flag
    elif flag == 1 and localflag != flag:
        import canadaMatcher
        from canadaMatcher import getLink # this function is abstracted so that the rules to define when we see a particular unknown case, we send them the link
        from canadaMatcher import links
        localflag = flag#this is done so that, if we build canada games matcher, we shouldn't be building it again
    matches, doc = extractKeywords(question)
    polite = False
    for match_id, start, end in matches:
        if "openerGreet".__contains__(nlp.vocab.strings[match_id]):
            polite = True
            break
    if multiQuestionCheck(matches, doc):
        processed = processKeywords(matches, doc)
        from queryTables import doQueries
        queryReturn = doQueries(processed)
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