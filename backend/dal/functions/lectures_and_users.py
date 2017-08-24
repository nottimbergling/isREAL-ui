from backend.dal.functions import dal_config
from backend.dal.mongo_client.mongodb_client import mongo_connection, get_all_documents_from_collection
from bson.objectid import ObjectId
import datetime

from backend.errors.bad_foramt_error import BadFormatError


def add_user(username, display_name, contact_details, availability=None, tags=None):
    if availability == None:
        availability = {dal_config.USERS_COLLECTION_AVAILABILITY_DAYS_KEY: [1, 2, 3, 4, 5], dal_config.USERS_COLLECTION_AVAILABILITY_HOURS_KEY: [9, 10, 11, 13, 14, 15, 16, 17]}
    if tags == None:
        tags = []
    insertion_data = {
        dal_config.USERS_COLLECTION_USERNAME_KEY: username,
        dal_config.USERS_COLLECTION_DISPLAY_NAME_KEY: display_name,
        dal_config.USERS_COLLECTION_CONTACT_DETAILS_KEY: contact_details,
        dal_config.USERS_COLLECTION_AVAILABILITY_KEY: availability,
        dal_config.USERS_COLLECTION_TAGS_KEY: tags
    }
    mongo_connection.users.insert_one(insertion_data)
    return insertion_data


def add_tag_for_user(username, tag_name):
    user = mongo_connection.users.find_one({dal_config.USERS_COLLECTION_USERNAME_KEY: username})
    user[dal_config.USERS_COLLECTION_TAGS_KEY].append(tag_name)
    mongo_connection.users.save(user)
    return user[dal_config.USERS_COLLECTION_TAGS_KEY]


def add_tag(tag_name, last_usage=None):
    if not last_usage:
        last_usage = datetime.datetime.utcnow()

    insertion_data = {
        dal_config.TAGS_COLLECTION_NAME_KEY: tag_name,
        dal_config.TAGS_COLLECTION_LAST_USAGE_KEY: last_usage
    }
    mongo_connection.tags.insert_one(insertion_data)
    return insertion_data

def get_all_users():
    all_users = mongo_connection.users.find({})
    return get_all_documents_from_collection(all_users)

def add_rating_for_user():
    pass


def add_review_for_lecture():
    pass


def add_tag_for_lecture():
    pass


def get_lectures_for_user(username):
    lectures_collection = mongo_connection.lectures.find({dal_config.LECTURES_COLLECTION_USERNAME_KEY: username})
    return get_all_documents_from_collection(lectures_collection)


def get_lectures():
    lectures_collection = mongo_connection.lectures.find({})
    return get_all_documents_from_collection(lectures_collection)


def get_user_data(username):
    user_data = mongo_connection.users.find({dal_config.USERS_COLLECTION_USERNAME_KEY: username})
    return user_data


def get_tags_for_user(username):
    user_data = get_user_data(username)
    return user_data[dal_config.USERS_COLLECTION_TAGS_KEY]


def get_user_contact_detail(username):
    user_data = get_user_data(username)
    return user_data[dal_config.USERS_COLLECTION_CONTACT_DETAILS_KEY]


def get_users():
    users_collection = mongo_connection.users.find({})
    return get_all_documents_from_collection(users_collection)


def get_lecture_tags():
    pass


def edit_user_data():
    pass


def create_new_lecture(title,username,description,tags,category):
    if title is None or username is None or description is None or tags is None or category is None:
        raise BadFormatError("cannot create new lecture with null parameters: title username description and tags")

    user_found = False
    for user in get_user_data(username):
        user_found=True
        break
    if user_found is False:
        raise BadFormatError("username: %s does not exist in the db" % username)


    insertion_data = {
        dal_config.LECTURES_COLLECTION_USERNAME_KEY: username,
        dal_config.LECTURES_COLLECTION_TITLE_KEY: title,
        dal_config.LECTURES_COLLECTION_DESCRIPTION_KEY: description,
        dal_config.LECTURES_COLLECTION_TAGS_KEY: tags,
        dal_config.LECTURES_COLLECTION_CATEGORY_KEY: category
    }
    added_document = mongo_connection.lectures.insert_one(insertion_data)
    return str(added_document.inserted_id)


def edit_lecture(lecture_id,title,username,description,tags,category):
    return lecture_id
    update_data = {
        dal_config.UNIQUE_ID_KEY : lecture_id,
        dal_config.LECTURES_COLLECTION_USERNAME_KEY: username,
        dal_config.LECTURES_COLLECTION_TITLE_KEY: title,
        dal_config.LECTURES_COLLECTION_DESCRIPTION_KEY: description,
        dal_config.LECTURES_COLLECTION_TAGS_KEY: tags,
    }
    mongo_connection.lectures.update(update_data)
    return lecture_id


def remove_tag_for_lecture():
    pass


def remove_tag_for_user():
    pass

def get_lecture_data(lecture_id):
    lectures_collection = mongo_connection.lectures.find({"_id" : ObjectId(lecture_id)})
    return get_all_documents_from_collection(lectures_collection)[0]

def get_all_tags():
    all_tags = mongo_connection.tags.find({})
    return get_all_documents_from_collection(all_tags)

def get_all_categories():
    all_categories = mongo_connection.categories.find({})
    return get_all_documents_from_collection(all_categories)