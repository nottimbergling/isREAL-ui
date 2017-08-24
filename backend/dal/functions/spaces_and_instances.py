from backend.dal.functions import dal_config
from backend.dal.mongo_client.mongodb_client import mongo_connection, get_all_documents_from_collection
from bson import ObjectId


def add_user_to_space():
    pass


def add_instance_to_space():
    pass


def add_review_for_instance():
    pass


def add_tag_for_instance():
    pass


def get_all_spaces():
    spaces_collection = mongo_connection.spaces.find({})
    return get_all_documents_from_collection(spaces_collection)


def get_my_spaces(username):
    spaces_collection = mongo_connection.spaces.find({dal_config.SPACES_COLLECTION_USERS_KEY: username})
    return get_all_documents_from_collection(spaces_collection)


def get_instances_for_space(space_id):
    lecture_instances_collection = mongo_connection.lecture_instances.find({dal_config.INSTANCES_COLLECTION_SPACE_ID_KEY: ObjectId(space_id)})
    return get_all_documents_from_collection(lecture_instances_collection)


def get_lecture_instances():
    lecture_instances_collection = mongo_connection.lecture_instances.find({})
    return get_all_documents_from_collection(lecture_instances_collection)


def get_tags_for_instance():
    pass


def edit_instance():
    pass


def remove_tag_for_instance():
    pass


def remove_user_from_space():
    pass

