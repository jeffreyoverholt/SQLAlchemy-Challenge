from flask import Flask, jsonify
from random import randint


app = Flask(__name__)

hello_dict = {"Hello": "World!", "abc": 123}


@app.route("/")
def home():
    return "Hi"



@app.route("/normal")
def normal():
    return hello_dict


@app.route("/jsonified")
def jsonified():
    return jsonify(hello_dict)


if __name__ == "__main__":
    app.run(debug=True)
