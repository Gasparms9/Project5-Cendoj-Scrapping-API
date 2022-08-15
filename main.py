from bson.json_util import dumps
import random

from bson.json_util import dumps
from flask import Flask, jsonify
from flask import Flask, redirect, url_for, request, render_template, make_response
from Tools.mongo_tools import all_sentences_byname
import markdown.extensions.fenced_code
from Tools.sql_tools import *

app = Flask(__name__)

@app.route("/")
def index():
    readme_file = open("README.md", "r")
    md_template = markdown.markdown(readme_file.read(), extensions = ["fenced_code"])
    return md_template


@app.route("/all")
def all_from_sql():
    try:
        lines = get_all_from_sql()
        return jsonify(lines)
    except Exception as e:
        return dumps({'error': str(e)})

@app.route("/random-number")
def random_number():
    return str(random.choice(range(0,1000)))


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



@app.route("/post/", methods=['POST', 'GET'])
def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        link = request.form.get("fname")
        downloading_sentence(link)
        data_sentencia = regex_court_sentence_file()
        uploading_sql(data_sentencia)
        return jsonify(data_sentencia)
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
