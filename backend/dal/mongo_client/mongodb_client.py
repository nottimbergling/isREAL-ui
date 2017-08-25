from bson import ObjectId
from pymongo import MongoClient
from backend import config
import datetime

# Authentication mechanisms
SCRAM_SHA_1 = "SCRAM-SHA-1"
MONGODB_CR = "MONGODB-CR"


class MongoDb(object):
    def __init__(self, host, database, port=27017, user=None, password=None, mechanism=SCRAM_SHA_1):
        connection = MongoClient(host=host, port=port)
        self.db = connection[database]
        if user and password:
            self.db.authenticate(user, password, mechanism=mechanism)


def _recursive_convert_object_id_to_string(document):
    if isinstance(document, ObjectId):
        return str(document)
    if isinstance(document, list):
        for value in document:
            value = _recursive_convert_object_id_to_string(value)
    if isinstance(document, dict):
        for key in document:
            document[key] = _recursive_convert_object_id_to_string(document[key])
    if isinstance(document, datetime.date):
        # return datetime.datetime.strftime(document, '%Y-%m-%d %H:%M:%s')
        return str(document)
    return document


def get_all_documents_from_collection(collection):
    documents = []
    for document in collection:
        document = _recursive_convert_object_id_to_string(document)
        documents.append(document)

    return documents


def run_function(function_name):
    function = mongo_connection.system.js.find_one({'_id': function_name})["value"]
    return mongo_connection.eval(function, "daniel")


mongo_connection = MongoDb(config.mongo_server, config.database, config.port).db
