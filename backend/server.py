from flask import Flask, render_template, request, json
from backend import botNLP as bN


app = Flask(__name__)
@app.route('/',methods = ['GET'])
def tester():
    return "hello this is flask and this is getting thigs"

@app.route("/",methods = ['GET'])
def frontend():
    return render_template("index.html")

@app.route("/", methods = ['POST'])
def front():
    return bN.processQ(json.loads(request.data)['message'])

if __name__ == "__main__":
    app.run(debug=True,port=5000)