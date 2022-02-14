from flask import Flask

app = Flask(__name__)

@app.route("/")
def front():
    return "test"

if __name__ == "__main__":
    app.run(debug=True,port=4000)