from argparse import ONE_OR_MORE
import pymongo
from pymongo import MongoClient
import sqlalchemy as alch
import os
import dotenv

dotenv.load_dotenv()

dburl = os.getenv("URL")

if not dburl:
    raise ValueError ("NO URL for database")

client = MongoClient(dburl)
db = client.get_database("Ironhack")
harrypotter_collection = db.get_collection("HP")
one_hp = harrypotter_collection.find_one()
print(one_hp)


