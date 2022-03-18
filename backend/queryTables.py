import sqlite3
import server
from flask_sqlalchemy import SQLAlchemy

# keywords is a dictionary of match_id and match_text
def doQueries(keywords):
    # print(keywords)
    if 'prereqs' in keywords or 'general question' in keywords or 'xlist' in keywords:
        try:
            print(keywords)
            print(keywords.get('course code'))
            filterCourseInputs(keywords)
            # temp = server.Course.query.filter_by(code='COSC4P03').first()
            # print(temp.description)
            print(server.Course.query.filter_by(code=keywords.get('course code')).first())
        except AttributeError:
            print('Attribute Error')
            return 'more info required'
        except:
            print('im in danger')
            return 'im in danger'
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
    temp = keywords.get('course code').text
    temp = temp.upper()
    print('filtered input: '+temp)
    keywords['course code'] = temp
    return None