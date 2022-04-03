import json

filename = "examtimetable.txt"
f = open(filename, 'r')
for line in f.readlines():
    temp = json.load(line)
    print(json.dumps(temp))