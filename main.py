from bson.json_util import dumps
import random

from bson.json_util import dumps
from flask import Flask, jsonify

from Tools.mongo_tools import all_sentences_byname

print(all_sentences_byname("Albus Dumbledore"))
app = Flask(__name__)


@app.route("/")
def greeting():
    return f"How are you doing"

from Tools.sql_tools import *
@app.route("/all")
def all_from_sql():
    try:
        lines = get_all_from_sql()
        return jsonify(lines)
    except Exception as e:
        return dumps({'error': str(e)})

@app.route("/count/<variable>")
def count_with_variable(variable):
    try:
        lines = get_count_with_variable(variable)
        return jsonify(lines)
    except Exception as e:
        return dumps({'error': str(e)})

@app.route("/all/<variable>/<name>")
def all_with_variable(variable, name):
    try:
        lines = get_all_with_variable(variable, name)
        return jsonify(lines)
    except Exception as e:
        return dumps({'error': str(e)})

@app.route("/post/<url>")
def post_sql(url):
    try:
        downloading_sentence(url)
        data_sentence = regex_court_sentence_file()
        uploading_sql(data_sentence)




@app.route("/random-number")
def random_number():
    return str(random.choice(range(0, 11)))


@app.route("/campus/<location>")
def campus_location(location):
    if location == "bcn":
        return "Carrer Pamplona 96"
    elif location == "mad":
        return "Madrid"

if __name__ == '__main__':
    app.run(debug=True)
