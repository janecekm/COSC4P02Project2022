import models
from flask_sqlalchemy import SQLAlchemy

# keywords is a dictionary of match_id and match_text
def doQueries(keywords):
    # print(keywords)
    if 'prereq' in keywords or 'general question' in keywords or 'xlist' in keywords:
        # try:
            print(keywords)
            print(keywords.get('code'))
            filterCourseInputs(keywords)
            # temp = server.Course.query.filter_by(code='COSC4P03').first()
            # print(temp.description)
            temp = models.Course.query.filter_by(code=keywords.get('code')).first()
            print(temp.prereq)
            temptemp = to_dict(temp)
            queryReturn = {}
            for key in (keywords.keys() & temptemp.keys()):
                print("attempting to add query return")
                queryReturn[key] = temptemp[key]
                print("query return add successful")
            print('Query Returned to botNLP: ')
            print(queryReturn)
            return queryReturn
        # except AttributeError:
        #     print('Attribute Error')
        #     print(keywords)
        #     return 'more info required'
        # except:
        #     print('im in danger')
        #     return 'im in danger'
    elif 'location' in keywords:
        print(keywords)
        try:
            if 'course code' in keywords:
                filterCourseInputs(keywords)
            elif 'building' in keywords:
                print('building found')
                return 'placeholder return'
            else:
                print('more info required')
                return 'more info required'
        except:
            print('location not found')
            return 'not found'
    # print(server.Course.query.all())
    return 'placeholder return'

# filter to match database formatting
def filterCourseInputs(keywords):
    temp = keywords.get('code').text
    temp = temp.upper()
    print('filtered input: '+temp)
    keywords['code'] = temp
    return None

def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}