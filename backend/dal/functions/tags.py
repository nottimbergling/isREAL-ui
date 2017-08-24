import datetime

from bson import ObjectId

from backend.dal.mongo_client.mongodb_client import mongo_connection, get_all_documents_from_collection


def add(name):
    insertion_data = {
        "_id": name,
        "rating": 1,
        "CreationDate": datetime.datetime.now()
    }
    mongo_connection.tags.insert_one(insertion_data)
    return insertion_data


def change_rating(name, amount):
    tag = mongo_connection.tags.find_one({"_id": ObjectId(name)})
    return mongo_connection.tags.update_one({"_id": ObjectId(name)}, {"rating": tag["rating"] + amount})


def delete(name):
    mongo_connection.tags.delete({"_id": ObjectId(name)})


def get_all():
    tags = mongo_connection.tags.find({},sort=[("rating", -1)])
    return get_all_documents_from_collection(tags)
