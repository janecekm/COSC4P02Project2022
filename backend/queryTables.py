import models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

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
                queryReturn[key] = queryRow[key]
            print('Query Returned to botNLP: ')
            print(queryReturn)
            return queryReturn
        except AttributeError:
            print('Attribute Error')
            print(keywords)
            return 'more info required'
        except Exception as e:
            print(e)
            return 'more info required'
    elif 'location' in keywords:
        try:
            if 'code' in keywords:
                filterCourseInputs(keywords)
                print(models.Offering.query.filter_by(code='COSC1P03').first())
                temp = models.Offering.query.filter_by(code=keywords.get('code')).all()
                # temp = models.Offering.query.filter_by(code=keywords.get('code')).first()
                for t in temp:
                    print(t.code)
                    print(t.frmt)
                print(temp)
                queryRow = to_dict(temp)
                queryReturn = {}
                for key in (keywords.keys() & queryRow.keys()):
                    queryReturn[key] = queryRow[key]
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
            print('location not found')
            return 'not found'
    return 'placeholder return'

# filter to match database formatting
def filterCourseInputs(keywords):
    temp = keywords.get('code').text
    temp = temp.upper().replace(" ","")
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