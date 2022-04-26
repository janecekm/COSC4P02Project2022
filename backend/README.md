# Backend Infrastructure
Our backend is uses technologies such as, flask, flask-sqlalchemy, pytest, docker, spacy, symspell, coverage and heroku. 
## Flask
Flask is a web development framework build for python. It helps simplify handling server process such as serving front end, doing backend processes and so on. More documentation can be read [here](https://flask.palletsprojects.com/en/2.1.x/)

The files that use this are 
- [Server](server.py)
- [Development Server](devserver.py)

where get and post requests are handled seperately by different processes, which helps which maintaining segmentation between backend and front end.

So the way the we can run is by running the command. 

>`python ./devserver.py`

this will run the development server, which uses files build by the npm from chatbot folder into static folder.

However, when the server is ready to be deployed into different environment, it is made into a container by using docker. The server is run by the container when in the deployment enviroment, however, if testing or improvements are done, the  devserver is the file that needs to be run.

## Pytest

This framework is used to perform testing for our software. You can read more documentation [here](https://docs.pytest.org/en/7.1.x/) . The way this works is it finds the files which starts from test_*.py . We have split the testing files into componenets so that we can test and know which function is not producing results that we need.

The commands to run if you are on windows is.
> python -m pytest .

However, if you have linux environment installed, the command to run is.
> pytest .

