from flask import Flask, render_template, request, json

app = Flask(__name__)

@app.route("/",methods = ['GET'])
def frontend():
    return render_template("index.html")

@app.route("/", methods = ['POST'])
def front():
    t = str(json.loads(request.data)['message']).rstrip()
    print(t)
    return {"message": str(json.loads(request.data)['message']).rstrip()}

if __name__ == "__main__":
    app.run(debug=True,port=5000)