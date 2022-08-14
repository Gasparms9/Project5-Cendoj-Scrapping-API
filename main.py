from flask import Flask, render_template, request
from bson.json_util import dumps
import random
import requests
from pymongo import MongoClient
import json
from Tools.mongo_tools import all_sentences_byname
from Config.mongo_config import harrypotter_collection
from os import name
from flask import Flask, request, jsonify
import markdown.extensions.fenced_code
import json
import random

print(all_sentences_byname("Albus Dumbledore"))
app = Flask(__name__)


@app.route("/")
def greeting():
    return f"How are you doing"


@app.route("/line/<name>")
def all_from_mongo(name):
    try:
        lines = all_sentences_byname(name)
        return jsonify(lines)
    except Exception as e:
        return dumps({'error': str(e)})


@app.route("/random-number")
def random_number():
    return str(random.choice(range(0, 11)))


@app.route("/campus/<location>")
def campus_location(location):
    if location == "bcn":
        return "Carrer Pamplona 96"
    elif location == "mad":
        return "Madrid"



app.run()