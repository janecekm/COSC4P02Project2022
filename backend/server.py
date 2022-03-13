from flask import Flask, render_template, request, json
import botNLP as bN
import os

app = Flask(__name__)

@app.route("/canada",methods=['GET'])
def canadafront():
    return render_template("index.html")

@app.route("/brock",methods = ['GET'])
def frontend():
    return render_template("index.html")

@app.route("/brock", methods = ['POST'])
def front():
    print(json.loads(request.data)['message'])
    return bN.processQ(json.loads(request.data)['message'])
@app.route("/",methods=['GET'])
def splashart():
    return render_template("splash.html")

# placeholder for now
if __name__ == "__main__":
    if "PORT" in os.environ:
        connectingport = os.environ.get("PORT")
    else:
        connectingport = 5000
    app.run(host="0.0.0.0", port=connectingport)