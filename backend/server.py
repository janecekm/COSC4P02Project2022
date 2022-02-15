from flask import Flask, render_template, request, json


app = Flask(__name__)
@app.route('/',methods = ['GET'])
def tester():
    return "hello this is flask and this is getting thigs"

@app.route("/", methods = ['POST'])
def front():
    print(json.loads(request.data)['message'])
    return {"message":"testing is good"}

if __name__ == "__main__":
    app.run(debug=True,port=5000)