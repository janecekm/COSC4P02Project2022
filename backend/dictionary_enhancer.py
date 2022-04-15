#put this in a folder
import json
import os
import platform

from symspellpy import SymSpell

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = "nlp-resources/frequency_dictionary_en_82_765.txt"
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

#pull coursecodes from webscrape into a list and iterate through it

#words for code numbers ex: 1p02
#words for course codes ex: COSC
#pandemic words: covid, covid-19, corona
wordList = ["covid", "covid-19", "coronavirus"]
'''
courseList = ["abed","abte","actg","aded","admi","adst","aesl","apco","arab","astr","bchm",
              "biol","bmed","bphy","btec","btgd","cana","chem","chys","clas","comm","cosc",
              "cpcf","dart","econ","edbe","educ","encw","engl","ensu","entr","ersc","esci",
              "ethc","film","fnce","fren","geog","germ","gree","hist","hlsc","iasc","indg",
              "intc","ital","itis","japa","kine","labr","lati","ling","mand","mars","math",
              "mgmt","mktg","musi","neur","nusc","obhr","oevi","oper","pcul","phil","phys",
              "pmpb","poli","port","psyc","recl","russ","scie","sclc","soci","span","spma",
              "stac","swah","tour","visa","wgst","wrds"]
'''
if os.path.basename(os.getcwd()) == "backend" and platform.system()=="Windows":
    path = ".\\nlp-resources\\"
elif os.path.basename(os.getcwd()) == "COSC4P02Project2022" and platform.system()=="Windows":
    path = ".\\backend\\nlp-resources\\"
elif os.path.basename(os.getcwd()) == "backend" and platform.system()=="Linux":
    path = "./nlp-resources/"
else:
    path = "./backend/nlp-resources/"

buildingList = []
with open(path+"buildingCodesClean.txt", encoding="utf8") as f:
    for line in f:
        buildingList.append(json.loads(line)["buildingCode"])

#print("is ", 8569404971)
for code in buildingList:
    print(str(code).lower(),101338951)