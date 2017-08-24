import datetime

from bson import ObjectId

from backend import dal
from backend.dal.functions import tags
from backend.dal.mongo_client.mongodb_client import mongo_connection, get_all_documents_from_collection


def add(tweetid, tags, author_display_name, author_user_name, author_id, likes, retweets, posting_time, search_type):
    insertion_data = {
        "_id": tweetid,
        "tags": tags,
        "authorDisplayName": author_display_name,
        "authorUserName": author_user_name,
        "authorId": author_id,
        "exposure": [{datetime.datetime.now().strftime("%Y:%m:%d %h:%M:%S"): {"likes": likes, "retweets": retweets}}],
        "postingTime": posting_time,
        "creationDate": datetime.datetime.now().strftime("%Y:%m:%d %h:%M:%S"),
        "searchType": search_type,
        "votes": 0
    }

    for tag in tags:
        dal.functions.tags.change_rating(tag, 1)

    mongo_connection.posts.insert_one(insertion_data)
    return True


def delete(post_id):
    mongo_connection.posts.delete({"_id": ObjectId(post_id)})


def vote(post_id, value):
    post = mongo_connection.posts.find_one({"_id": post_id})
    mongo_connection.posts.update_one({"_id": post_id}, {"$set": {"votes": post["votes"] + value}})
    for tag in post["tags"]:
        tags.change_rating(tag,value)
    return True


def get_new(tags=None, author=None):
    search_dict = {}
    if tags or author:
        search_dict["$or"] = []
    if tags:
        for tag in tags:
            search_dict["$or"].append({"tags": {"$regex": tag, "$options": "i"}})
    if author:
        search_dict["author"] = {"$regex": author, "$options": "i"}

    posts = mongo_connection.posts.find(search_dict, sort=[("postingTime", -1)]).limit(20)
    return get_all_documents_from_collection(posts)


def get_hot(tags, author):
    # search_dict = {"creationDate": {"$gt": datetime.datetime.now() - datetime.timedelta(days=30)}}
    search_dict = {}
    if tags or author:
        search_dict["$or"] = []
    if tags:
        for tag in tags:
            search_dict["$or"].append({"tags": {"$regex": tag, "$options": "i"}})
    if author:
        search_dict["author"] = {"$regex": author, "$options": "i"}

    posts = mongo_connection.posts.find(search_dict)
    posts = sorted(posts, key=rate_posts, reverse=True)
    return get_all_documents_from_collection(posts)


def rate_posts(match):
    return 1
