import json

f = open("buildingCodesCleaned.txt",'r')
for line in f.readlines():
    print(json.dumps(line))
