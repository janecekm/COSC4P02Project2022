import models

# keywords is a dictionary of match_id and match_text
# print(models.Course.query.all())
def doQueries(keywords):
    if 'prereq' in keywords or 'description' in keywords or 'xlist' in keywords:
        try:
            filterCourseInputs(keywords)
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
    elif 'exam' in keywords:
        try:
            if 'code' in keywords:
                print("KEYWORDS: ")
                print(keywords)
                filterCourseInputs(keywords)
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
    elif 'location' in keywords or 'instructor' in keywords or 'time' in keywords or 'course component' in keywords:
        try:
            if 'code' in keywords:
                filterCourseInputs(keywords)
                temp = models.Offering.query.filter_by(code=keywords.get('code')).all()
                # temp = models.Offering.query.filter_by(code=keywords.get('code')).first()
                print(temp)
                queryReturn = {}
                for row in temp:
                    queryRow = to_dict(row)
                    rowDict = {}
                    for key in (keywords.keys() & queryRow.keys()):
                        if key == 'time':
                            rowDict['days'] = queryRow["days"]
                        rowDict[key] = queryRow[key]
                    queryReturn.update(rowDict)
                print('Query Returned to botNLP: ')
                print(queryReturn)
                return queryReturn
            elif 'building' in keywords:
                print('building found')
                return 'placeholder return'
            else:
                print('more info required')
                return 'more info required'
        except Exception as e:
            print(e)
            return 'not found'
    return 'placeholder return'

# filter to match database formatting
def filterCourseInputs(keywords):
    temp = keywords.get('code').text
    temp = temp.upper()
    print('filtered input: '+temp)
    keywords['code'] = temp
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