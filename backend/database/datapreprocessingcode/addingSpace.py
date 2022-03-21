import json

f = open("../timetable.txt",'r')
k = open("timetablenext.txt",'w+')
for line in f.readlines():
    f = json.loads(line)
    coursecode = ""
    num = 0
    for chr in f['cc']:
        if(ord(chr)>57):#if it is not a number
            coursecode = coursecode + chr
            num +=1
        else:
            break
    f['cc'] = coursecode+" "+str(f['cc'][num:]) # this is the line
    k.write(json.dumps(f)+"\n")