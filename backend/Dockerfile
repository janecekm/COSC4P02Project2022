FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY . /
RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_md

CMD ["python3","server.py"]