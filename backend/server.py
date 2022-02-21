from flask import Flask, render_template, request, json
import botNLP as bN
import time

app = Flask(__name__)

@app.route("/canada",methods=['GET'])
def canadafront():
    return render_template("index.html")

@app.route("/brock",methods = ['GET'])
def frontend():
    return render_template("index.html")

@app.route("/brock", methods = ['POST'])
def front():
    time.sleep(2)
    return bN.processQ(json.loads(request.data)['message'])

if __name__ == "__main__":
    app.run(debug=True,port=5000)