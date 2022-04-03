#takes the buildingCodes.txt and formats it so that 
# it prints {"buildingCode":"", "buildingName":""}

import json

f = open("buildingCodes.txt","r")
file = json.load(f)
flag = False
for key in file.keys():
    temp = {"buildingCode":"","buildingName":""}
    if flag:
        temp["buildingCode"] = key
        temp["buildingName"] = file[key]
        print(json.dumps(temp))
    else:
        flag = True