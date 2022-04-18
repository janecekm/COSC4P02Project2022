import models
import re
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
            temp = models.Building.query.filter_by(code=keywords.get('buildingCode')).all()
            print(temp)
            queryReturn = {}
            for row in temp:
                queryRow = to_dict(row)
                rowDict = {}
                for key in (keywords.keys() & queryRow.keys()):
                    rowDict[key] = queryRow[key]
                rowDict["code"] = queryRow["code"]
                rowDict["name"] = queryRow["name"]
                queryReturn.update(rowDict)
            print('Query Returned to botNLP: ')
            print(queryReturn)
            return queryReturn
        except Exception as e:
            print(e)
            print('building not found')
            return 'not found'
    #Course table, code must be in keywords
    elif 'prereq' in keywords or 'description' in keywords or 'xlist' in keywords:
        try:
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
            return 'more info required'
        except Exception as e:
            print(e)
            return 'more info required'
    #Exam table
    elif 'exam' in keywords:
        try:
            if 'code' in keywords:
                print("KEYWORDS: ")
                print(keywords)
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
            return 'not found'
    #Offering table
    elif 'location' in keywords or 'instructor' in keywords or 'time' in keywords or 'format' in keywords:
        try:
            if 'code' in keywords:
                keywords['code'] = filterInputs(keywords, 'code')
                temp = models.Offering.query.filter_by(code=keywords.get('code')).all()
                # temp = models.Offering.query.filter_by(code=keywords.get('code')).first()
                print(temp)
                queryReturn = {}
                for row in temp:
                    queryRow = to_dict(row)
                    rowDict = {}
                    rowsList = []
                    for key in (keywords.keys() & queryRow.keys()):
                        rowDict = {}
                        if 'format' in keywords:
                            keywords["format"] = filterInputs(keywords, 'format')
                            if rowDict['format'] == queryRow['format']:
                                rowDict[key] = queryRow[key]
                        else:
                            if key == 'time':
                                rowDict[key] = queryRow[key]
                                rowDict['days'] = queryRow["days"]
                            else:
                                rowDict[key] = queryRow[key]
                        queryReturn.update(rowDict)
                        rowsList.append(rowDict)
                    print(rowsList)
                print('Query Returned to botNLP: ')
                print(queryReturn)
                return queryReturn
            else:
                print('more info required')
                return 'more info required'
        except Exception as e:
            print(e)
            return 'not found'
    return 'placeholder return'

# filter to match database formatting
def filterInputs(keywords, key):
    temp = keywords.get(key).text
    temp = temp.upper()
    temp = re.split(r'([0-9][A-Z][0-9][0-9])', temp, maxsplit=1)
    temp = [t.strip() for t in temp]
    temp = ' '.join(temp).strip()
    print('filtered input: '+temp)
    # keywords[key] = temp
    return temp

def filterBuildingCodes(keywords):
    temp = keywords.get('buildingCode').text
    temp = temp.upper()
    temp = re.split(r'([0-9][A-Z][0-9][0-9])', temp, maxsplit=1)
    temp = [t.strip() for t in temp]
    temp = ' '.join(temp).strip()
    print('filtered input: '+temp)
    keywords['buildingCode'] = temp
    return None

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