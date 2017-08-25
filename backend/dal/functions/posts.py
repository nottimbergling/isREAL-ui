import datetime

from bson import ObjectId

from backend import dal
from backend.dal.functions import tags
from backend.dal.mongo_client.mongodb_client import mongo_connection, get_all_documents_from_collection
from backend.nlp import get_knn_model


def add(tweetid, text, tags, author_display_name, author_user_name, author_id, author_followers, likes, retweets,
        posting_time, search_type):
    insertion_data = {
        "_id": tweetid,
        "text": text,
        "tags": tags,
        "authorDisplayName": author_display_name,
        "authorUserName": author_user_name,
        "authorId": author_id,
        "authorFollowers": author_followers,
        "exposure": [{datetime.datetime.now().strftime("%Y:%m:%d %h:%M:%S"): {"likes": likes, "retweets": retweets}}],
        "postingTime": posting_time,
        "creationDate": datetime.datetime.now().strftime("%Y:%m:%d %h:%M:%S"),
        "searchType": search_type,
        "votes": 0
    }

    for tag in tags:
        dal.functions.tags.change_rating(tag, 1)

    dal.functions.authors.change_rating(author_display_name, 1)

    mongo_connection.posts.insert_one(insertion_data)
    return True


def delete(post_id):
    mongo_connection.posts.delete({"_id": ObjectId(post_id)})


def vote(post_id, value):
    post = mongo_connection.posts.find_one({"_id": post_id})
    mongo_connection.posts.update_one({"_id": post_id}, {"$set": {"votes": post["votes"] + value}})
    for tag in post["tags"]:
        tags.change_rating(tag, value)

    dal.functions.authors.change_rating(post["author"], 1)
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
    posts = sort_posts(posts)
    # posts = sorted(posts, key=rate_posts, reverse=True)
    return get_all_documents_from_collection(posts)


def sort_posts(posts):
    # status_to_data[status.id] = [status.text, status.favorite_count, status.retweet_count, status.user.followers_count]
    status_to_data = dict()
    id_to_post = dict()
    posts = [p for p in posts]
    for post in posts:
        tweet_id = post["_id"]
        text = post["text"]
        likes = list(post["exposure"][-1].values())[-1]['likes']
        retweets = list(post["exposure"][-1].values())[-1]['retweets']
        followers = post["authorFollowers"]
        id_to_post[tweet_id] = post
        status_to_data[tweet_id] = [text, likes, retweets, followers]

    ordered_ids = get_knn_model(status_to_data)
    ordered_posts = [id_to_post[ordered_id] for ordered_id in ordered_ids]

    return ordered_posts

def rate_posts(post):
    return 1
