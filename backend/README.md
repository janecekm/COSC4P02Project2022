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
 
 The naming convention we use is 
 > test_sitename_function.py

 Then we use a package called coverage to test how much of the code is tested by the tests we have set up.

 ## Coverage

This is a framework developed to help developers measure how much of the code has been tested by the [pytest](#pytest) framework. You can read more about Coverage [here](https://coverage.readthedocs.io/en/6.3.2/)

The way this is run is by,

For windows 
> python -m coverage run -m pytest .

For linux environment
> coverage run -m pytest .

Then there are many ways to view the final report. The command line version of it is by,
>coverage report

## Docker
Docker is an amazing tool, which can be used to containarize software and easily be able to be deployed into different environment or platforms. 

You can read more about docker [here](https://www.docker.com/)

The file in which our image is contained is -

- [DockerFile](../Dockerfile)

This has to exist in the most external folder so that the ennvironment we are deploying into can grab that file easily.



