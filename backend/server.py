import json
from flask import Flask, request

app = Flask(__name__)
@app.route('/',methods = ['GET'])
def tester():
    return "hello this is flask and this is getting thigs"

@app.route('/', methods =['POST'])
def test():
    t = json.loads(request.data)
    print(t['message'])
    return ">test<"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
