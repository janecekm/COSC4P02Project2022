import json

f = open("course.txt","r")
file = json.load(f)
clean = open ("courseClean.txt", "w")
clean.write(json.dumps(file))