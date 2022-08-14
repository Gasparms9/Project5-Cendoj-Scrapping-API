from Config.mongo_config import harrypotter_collection

# get
one = harrypotter_collection.find_one()
print(one)


def all_sentences_byname(name):  ## name we pass
    ## function to get info
    query = {"character_name": f"{name}"}
    sent = list(harrypotter_collection.find(query, {"_id": 0}))
    return sent


print(list(all_sentences_byname("Albus Dumbledore")))


## insert into the database

def inserting(dict_):
    harrypotter_collection.insert_one(dict_)
    return f"I inserted {dict_} into the db"

