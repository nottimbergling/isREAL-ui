def get_all():
    authors = mongo_connection.authors.find({}, sort=[("rating", -1)])
    return get_all_documents_from_collection(authors)


import datetime

from bson import ObjectId

from backend.dal.mongo_client.mongodb_client import mongo_connection, get_all_documents_from_collection


def add(name):
    insertion_data = {
        "_id": name,
        "rating": 1,
        "CreationDate": datetime.datetime.now()
    }
    mongo_connection.authors.insert_one(insertion_data)
    return insertion_data


def change_rating(name, amount):
    author = mongo_connection.tags.find_one({"_id": name})
    new_rating = 1
    if author is not None:
        new_rating = author["rating"] + amount

    mongo_connection.authors.update_one({"_id": name}, {"$set": {"rating": new_rating}}, upsert=True)




def delete(name):
    mongo_connection.authors.delete({"_id": ObjectId(name)})
