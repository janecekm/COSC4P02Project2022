import json
f = open("course.txt","r")
for line in f.readlines():
    a = json.loads(line)
    try:
        a["xlist"] = a["xlist"][:len(a["xlist"])-1]
    except:
        pass
    print(json.dumps(a))