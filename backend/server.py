from flask import Flask

app = Flask(__name__)

@app.route("/")
def front():
    print("test")
    return "test"

if __name__ == "__main__":
    app.run(debug=True,port=4000)