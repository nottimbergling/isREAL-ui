import datetime

from bson import ObjectId

from backend.dal.mongo_client.mongodb_client import mongo_connection, get_all_documents_from_collection


def add(url, tags, author, likes, retweets, posting_time):
    insertion_data = {
        "url": url,
        "tags": tags,
        "author": author,
        "exposure": [{datetime.datetime.now(): {"likes": likes, "retweets": retweets}}],
        "postingTime": posting_time,
        "CreationDate": datetime.datetime.now()
    }
    mongo_connection.posts.insert_one(insertion_data)
    return insertion_data


def delete(post_id):
    mongo_connection.posts.delete({"_id": ObjectId(post_id)})


def get_new():
    posts= mongo_connection.posts.find({}, sort=[("postingTime", -1)])
    return get_all_documents_from_collection(posts)


def get_hot():
    posts = mongo_connection.posts.find({})
    sorted(posts,key=rate_posts, reverse=True)
    return get_all_documents_from_collection(posts)


def rate_posts():
    return 1