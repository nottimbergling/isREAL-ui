from backend.dal.mongo_client.mongodb_client import mongo_connection, get_all_documents_from_collection
import time

def add(originalid, retweetid, userid):
    timestamp = time.time()
    insertion_data = {
        "_id": retweetid,
        "user": userid,
        "post": originalid,
        "timestamp": timestamp
    }
    mongo_connection.comments.insert_one(insertion_data)
    return True


def get_comments_by_user(userid):
    comments = mongo_connection.comments.find({"user": userid}, sort=[("timestamp", -1)])
    return get_all_documents_from_collection(comments)


def get_comments_by_tweet(tweetid):
    comments = mongo_connection.comments.find({"post": tweetid}, sort=[("timestamp", -1)])
    return get_all_documents_from_collection(comments)
