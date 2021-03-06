import models
import re
import json
# keywords is a dictionary of match_id and match_text
# print(models.Course.query.all())
def doQueries(keywords):
    print("Keywords received from botNLP: ")
    print(keywords)
    #Builing table
    if 'buildingCode' in keywords:
        try:
            print(keywords)
            keywords['code'] = filterInputs(keywords, 'buildingCode')
            temp = models.Building.query.filter_by(code=keywords.get('code')).all()
            print(temp)
            queryReturn = {}
            for row in temp:
                queryRow = to_dict(row)
                rowDict = {}
                for key in (keywords.keys() & queryRow.keys()):
                    rowDict[key] = queryRow[key]
                rowDict["buildingCode"] = queryRow["code"]
                rowDict["name"] = queryRow["name"]
                queryReturn.update(rowDict)
            print('Query Returned to botNLP: ')
            print(queryReturn)
            return queryReturn
        except Exception as e:
            print(e)
            print('building not found')
            # return None
    #Course table, code must be in keywords
    elif 'prereq' in keywords or 'description' in keywords or 'xlist' in keywords:
        try:
            if 'code' in keywords:
                keywords['code'] = filterInputs(keywords, 'code')
                temp = models.Course.query.filter_by(code=keywords.get('code')).first()
                queryRow = to_dict(temp)
                queryReturn = {}
                for key in (keywords.keys() & queryRow.keys()):
                    if key == 'description': queryReturn['title'] = queryRow['title']
                    queryReturn[key] = queryRow[key]
                print('Query Returned to botNLP: ')
                print(queryReturn)
                return queryReturn
        except AttributeError as a:
            print(a)
            print(keywords)
            # return None
        except Exception as e:
            print(e)
            # return None
    #Exam table
    elif 'exam' in keywords:
        try:
            if 'code' in keywords:
                keywords['code'] = filterInputs(keywords, 'code')
                temp = models.Exam.query.filter_by(code=keywords.get('code')).all()
                queryReturn = {}
                print(temp)
                for row in temp:
                    queryRow = to_dict(row)
                    rowDict = {}
                    for key in (keywords.keys() & queryRow.keys()):
                        rowDict[key] = queryRow[key]
                    rowDict['exam'] = keywords["exam"]
                    rowDict['location'] = queryRow["location"]
                    rowDict['dayNum'] = queryRow["dayNum"]
                    rowDict['month'] = queryRow["month"]
                    rowDict['time'] = queryRow["time"]
                    queryReturn.update(rowDict)
                print('Query Returned to botNLP: ')
                print(queryReturn)
                return queryReturn
        except Exception as e:
            print(e)
            print('exam not found')
            # return None
    #Offering table
    elif 'location' in keywords or 'instructor' in keywords or 'time' in keywords or 'format' in keywords:
        try:
            if 'code' in keywords:
                keywords['code'] = filterInputs(keywords, 'code')
                temp = models.Offering.query.filter_by(code=keywords.get('code')).all()
                # temp = models.Offering.query.filter_by(code=keywords.get('code')).first()
                print(temp)
                queryReturn = {}
                rowsList = []
                if 'format' in keywords.keys():
                    # open the brockdictionary.json file to standardize the format of the course component
                    from botNLP import filepath
                    changer = open(filepath()+"brockdictionary.json","r") # loading the brock dictionary for word substitutions
                    changer = json.load(changer) # since we are using a json file, load instead of loads
                    keywords['format'] = filterInputs(keywords, 'format')
                    t = keywords['format'].lower() # converts into lower to match the dictionary.
                    keywords['format'] = changer[t].upper() # converts into uppper to match the database.
                for row in temp:
                    queryRow = to_dict(row)
                    rowDict = {}
                    for key in (keywords.keys() & queryRow.keys()):
                        if 'format' in keywords.keys():
                            if keywords['format'] == queryRow['format']:
                                if 'formatNum' in keywords.keys():
                                    if keywords['formatNum'] == queryRow['formatNum']:
                                        rowDict[key] = queryRow[key]
                                        rowDict['days'] = queryRow['days']
                                        rowDict['duration'] = queryRow['duration']
                                else:
                                    rowDict[key] = queryRow[key]
                                    rowDict['days'] = queryRow['days']
                                    rowDict['formatNum'] = queryRow['formatNum']
                                    rowDict['duration'] = queryRow['duration']
                        elif queryRow['format'] == 'LEC' or queryRow['format'] == 'SYN' or queryRow['format'] == 'ASY' or queryRow['format'] == 'BLD' or queryRow['format'] == 'HYF' or queryRow['format'] == 'PRO' or queryRow['format'] == 'INT' or queryRow['format'] == 'LEC2':
                            if key == 'time':
                                rowDict[key] = queryRow[key]
                                rowDict['days'] = queryRow["days"]
                                rowDict['duration'] = queryRow['duration']
                            else:
                                rowDict[key] = queryRow[key]
                                rowDict['duration'] = queryRow['duration']
                                if 'location' in keywords.keys():
                                    rowDict["days"] = queryRow["days"]
                        # if 'location' in keywords.keys():
                        #     rowDict["days"] = queryRow["days"]
                        # if rowDict:
                        #     queryReturn.update(rowDict)
                    if rowDict:
                        queryReturn.update(rowDict)
                        rowsList.append(rowDict)
                print(rowsList)
                for r in rowsList:
                    print(r)
                # if 'format' in keywords.keys():
                #     l = []
                #     for r in rowsList:
                #         # if r.get('location'):
                            
                #             print(r)
                print('Compressed Query Returned to botNLP: ')
                # print(queryReturn)
                compressed = compressList(rowsList)
                print(compressed)
                return rowsList
            else:
                print('more info required')
                # return None
        except Exception as e:
            print(e)
            # return None
    if 'programName' in keywords:
                try:
                    temp = models.Program.query.filter_by(program=keywords.get('programName')).first()
                    queryReturn = {}
                    if temp:
                        queryRow = to_dict(temp)
                        queryReturn["programName"] = queryRow["program"]
                        queryReturn["link"] = queryRow["link"]
                    else:
                        return None
                    print('Query Returned to botNLP: ')
                    print(queryReturn)
                    return queryReturn
                except Exception as e:
                    print(e)
                    # return None
    return None

def cgQueries(keywords):
    try:
        print(keywords)
        if "time" in keywords:
            temp = models.Schedule.query.filter_by(sport=keywords.get('sport').lower()).all()
            print(temp)
            rowsList = []
            for row in temp:
                queryRow = to_dict(row)
                rowDict = {}
                rowDict["month"] = queryRow["month"]
                rowDict["date"] = queryRow["date"]
                rowDict["time"] = queryRow["time"]
                rowDict["gender"] = queryRow["gender"]
                rowDict["sport"] = queryRow["sport"].capitalize()
                rowDict["venue"] = queryRow["venue"]
                rowsList.append(rowDict)
            return rowsList
        if "location" in keywords:
            temp = models.Schedule.query.filter_by(sport=keywords.get('sport').lower()).all()
            print(temp)
            rowsList = []
            for row in temp:
                queryRow = to_dict(row)
                rowDict = {}
                rowDict["venue"] = queryRow["venue"]
                rowDict["sport"] = queryRow["sport"].capitalize()
                rowDict["location"] = keywords["location"]
                rowsList.append(rowDict)
            return rowsList
        return None
    except Exception as e:
        print(e)
    return None

# filter to match database formatting
def filterInputs(keywords, key):
    temp = keywords.get(key)
    temp = temp.upper()
    temp = re.split(r'([0-9][A-Z][0-9][0-9])', temp, maxsplit=1)
    temp = [t.strip() for t in temp]
    temp = ' '.join(temp).strip()
    print('filtered input: '+temp)
    # keywords[key] = temp
    return temp

def filterBuildingCodes(keywords):
    temp = keywords.get('buildingCode')
    temp = temp.upper()
    temp = re.split(r'([0-9][A-Z][0-9][0-9])', temp, maxsplit=1)
    temp = [t.strip() for t in temp]
    temp = ' '.join(temp).strip()
    print('filtered input: '+temp)
    keywords['buildingCode'] = temp
    return None

def filterFormat(keywords):
    comp = ''
    num = ''
    barred = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    for i in range(len(keywords["format"])):
        if keywords["format"][i] in barred:
            num += keywords["format"][i]
        elif not i == " ":
            comp += keywords["format"][i]
    keywords['format'] = comp.strip()
    keywords['formatNum'] = num

def compressList(input):
    compressed = {}
    bookkeeping = []
    for row in input:
        for key in row:
            if not key in compressed:
                compressed[key] = row[key]
                bookkeeping.append(row[key])
            elif not row[key] == '' and not row[key] in bookkeeping:
                compressed[key] += ' & ' + row[key]
                bookkeeping.append(row[key])
                
    return compressed

def queryReturn(keywords, temp):
    queryRow = to_dict(temp)
    queryReturn = {}
    for key in (keywords.keys() & queryRow.keys()):
        queryReturn[key] = queryRow[key]
    print('Query Returned to botNLP: ')
    print(queryReturn)
    return queryReturn

# returns a dictionary of column and row corresponding to SQLAlchemy model object
def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}