
![badgerimage](chatbot/public/anotherbadger.png)
# COSC 4P02 Project 2022
A group project for Brock University's COSC 4P02 (Software Engineering 2).

### Chat Bot Application for Brock University and Canada Games
This project we developed is a web-based chatbot application that accomodates two distinct modes; One for Brock University and the other for Canada Games. We wanted to be able to provide a single website, where the user can ask questions that they have regarding that particular domain, i.e. Brock University or Canada Games, and be provided with meaningful answers. This maybe a link to the resource or an actual answer so that the user doesn't need to hunt for that information. 

## Tech Stack
For this project the primary technologies we used were:

| Technology | usage |
| -------- | --------- |
| [Python](https://www.python.org/) | [Backend](./backend/), [Datacleaning](./backend/database/datapreprocessingcode/) |
| [Selenium](https://www.selenium.dev/) | [Webscraping](./backend/web-scraping) |
| [React/javascript](https://reactjs.org/) | [Frontend](./chatbot/src) |
| [Node Package Manager](https://www.npmjs.com/) | [Frontend](./chatbot/)|
| [Flask](https://flask.palletsprojects.com/en/2.1.x/) | [Server](./backend/server.py) |
| [SpaCy](https://spacy.io/) | [NLP](./backend/botNLP.py) |
| [SQLite](https://www.sqlite.org/index.html) | [Database](./backend/models.py) |
| [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/_) | [Querying Database](./backend/queryTables.py) |
| [PyTest](https://docs.pytest.org/en/7.1.x/) | [Testing](./backend/) |
| [Coverage](https://coverage.readthedocs.io/en/6.3.2/) | [Coverage](./backend) |
| [Docker](https://www.docker.com/) | [containerization](./Dockerfile) |
| [Heroku](https://developer.salesforce.com/) | [Deployment](./heroku.yml) |

In addition to that, other installs that is required to run the project is in the [requirements.txt](./backend/requirements.txt) file.

### Team Members:
- Greg Pogue 4583993 (Team Leader)
- Joel Jacob 6603245
- Madeline Janecek 6436620
- Sam Langdon 6180137
- Brendan Park 6541288
- Kylee Schram 6131726

### Backend
The backend folder of this project consists of the following folders.
- Database
    * Cleandata Folder: consists of the cleaned data that has been 
    scraped from various resources such as Brock University and Canada Games
    websites.
    * Data PreProcessing Code: consists of the python scripts written to clean
    and prepare the data for usage in the database.
    * The '.db' files are used to store the cleaned data.
    * The '_init.sql' files format the data into tabular format for the database.
    * The 'input.py' files take the clean data and insert it into the database.
- NLP-Resources
    * This folder contains all files which the nlp code makes use of in order to accurately understand
    and respond to user queries. The frequency dictionary allows for the auto-correction of user input
    prior to its entry into the nlp pipeline. This allows us to easily read input that may have a
    few misspellings in it. There are also lists of links for questions in which we redirect the user
    to an external source for more detailed information. Finally, there is also a list of common locations
    or terms that are unique to each given chatbot such as town names or venue locations.
- Static
    * The static folder just contains parts for the front end such as the splash page as well as images
    displayed on the front-end.
- Templates
    * A folder of images and html code for the front-end
- Web-Scraping
    * This folder contains the various python scripts used to scrape data about Brock and Canada Games for
    future use in the database.
For more details about the backend refer to: [Backend-READ-ME](backend/README.md)

### Chatbot
This folder contains resources used for the front-end. This includes the css and js files as well as 
some images such as logos or icons. For more details about these documents please refer to
[Chatbot-READ-ME](chatbot/README.md)

### Documentation
This folder contains every piece of documentation for the chatbot project

### Other Documents
- Dockerfile
    * this file is used to build the container for our project so that it can be hosted via Heroku.
- Heroku.yml
    * This file is used to define which file is run when we host our project
