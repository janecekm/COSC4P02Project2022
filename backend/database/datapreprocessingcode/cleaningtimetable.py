import json

from numpy import DataSource

file = open("timetable.txt",'r', encoding="utf-16")
Days ={"M":"Monday","T":"Tuesday","W":"Wednesday","R":"Thursday","F":"Friday","S":"Saturday","Sun.":"Sunday"}
def addSpaceToLocations(locationName):
    numberInBuildingName = False
    location = ""
    roomNum = ""
    for n in locationName:
        if numberInBuildingName:#to indicate that there is a number in the building name _ or - followed by a nubmer
            location = location+n
            numberInBuildingName = False
            continue
        if n =="_" or n=="-":
            numberInBuildingName = True
        if ord(n)>=65:
            location = location+n
        else:

            roomNum = roomNum+n
    return location+" "+roomNum

for line in file.readlines():
    f = json.loads(line)
    coursecode = ""
    num = 0
    for chr in f['cc']:
        if(ord(chr)>57):#if it is not a number
            coursecode = coursecode + chr
            num +=1
        else:
            break
    temp = coursecode+" "+str(f['cc'][num:]) # this is the line
    f.pop("cc")
    f["courseCode"] = temp#changes teh courseCode
    
    day = f["days"]
    # print(day)
    locationName = f["loc"]
  

    locations = []# for specific locations
    num = 0
    temp = ""
    for s in f["loc"]:
        temp = temp+s
        if ord(s)<65:#it is not a letter
            num = num +1
        if num ==3:#3rd number
            num = 0
            locations.append(temp)
            temp = ""


    
    f["loc"] =  [addSpaceToLocations(x) for x in locations]#location has space
    f["room1"] = addSpaceToLocations(f["room1"])
    f["room2"] = addSpaceToLocations(f["room2"])

    datesExist = False # indicates if d
    for d in day:
        try:
            val = Days[d] # if not of the form
            # f["days"].append(val)
            f["days"] = val
            print(f)
            datesExist = True
        except:
            pass
    if not datesExist:
        f["days"] = ""
        print(f)
    # k.write(json.dumps(f)+"\n")