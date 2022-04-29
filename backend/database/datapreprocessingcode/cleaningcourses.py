import json
def run(filename): # the file name is the path to store the file in
    '''
    this function cleans up the courses crosslisting if there is cosc4p61)
    '''
    f = open(filename,"r")
    for line in f.readlines():
        a = json.loads(line)
        try:
            a["xlist"] = a["xlist"][:len(a["xlist"])-1]
        except:
            pass
        print(json.dumps(a))