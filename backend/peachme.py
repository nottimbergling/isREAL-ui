import inspect
import os
import sys

from flask import Flask, send_file, redirect

from backend import config, dal
from backend.adapters.request_adapter import request_adapter_wrapper
from backend.adapters.response_adapter import response_adapter_wrapper
from backend.config import frontend_path
from backend.entities.base_request import BaseRequest
from backend.logs.logger import logger

sys.path.append(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

# initialize Flask
app = Flask(__name__, static_folder="../")
logger.info(" ################## SEARCH STARTING ##################" +
            "\n - Configuration name: " + config.name)


@app.route("/")
@app.route("/search")
@app.route("/profile")
@app.route("/spaces")
@app.route("/lecture")
@app.route("/createlecture")
@app.route("/createuser")
@app.route("/loading")
@app.route("/404")
def index():
    return send_file(os.path.join(frontend_path, "index.html"))


@app.route("/profile/<user>")
def user(user):
    return send_file(os.path.join(frontend_path, "index.html"))


@app.route("/lecture/<id>")
def lecture(id):
    return send_file(os.path.join(frontend_path, "index.html"))


@app.route("/<path:path>")
def send_static_file(path):
    try:
        return app.send_static_file(path)
    except Exception as e:
        return redirect("/404")


@app.route('/posts/get/new', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def get_new_posts(request):
    tags = request.body.get("tags")
    author = request.body.get("author")
    return dal.functions.posts.get_new(tags, author)


@app.route('/posts/get/hot', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def get_hot_posts(request):
    tags = request.body.get("tags")
    author = request.body.get("author")
    return dal.functions.posts.get_hot(tags, author)


@app.route('/posts/vote', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def vote(request):
    vote_value = request.body["value"]
    post_id = request.body["postId"]
    return dal.functions.posts.vote(post_id, vote_value)


@app.route('/posts/add', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def create_post(request):
    url = request.body["url"]
    tags = request.body["tags"]
    author_user_name = request.body["authorUserName"]
    author_display_name = request.body["authorDisplayName"]
    author_id = request.body["authorId"]
    likes = request.body["likes"]
    retweets = request.body["retweets"]
    posting_time = request.body["tweetPostingTime"]

    return dal.functions.posts.add(url, tags, author_display_name, author_user_name, author_id, likes, retweets,
                                   posting_time)


@app.route('/posts/delete', methods=['PUT'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def delete_post(request):
    pass


@app.route('/tags/get', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def get_tags(request):
    return dal.functions.tags.get_all()


@app.route('/tags/add', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def add_tag(request):
    return dal.functions.tags.add(request.body["name"])


@app.route('/tags/delete', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def delete_tag(request):
    return dal.functions.tags.delete(request.body["name"])


@app.route('/tags/change_rating', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def rate_tag(request):
    return dal.functions.tags.change_rating(request.body["ratingDiff"])


@app.route('/authors/get', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def get_authors(request):
    return dal.functions.authors.get_all()


@app.route('/authors/add', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def add_author(request):
    return dal.functions.authors.add(request.body["name"])


@app.route('/authors/delete', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def delete_author(request):
    return dal.functions.authors.delete(request.body["name"])


@app.route('/authors/change_rating', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def rate_author(request):
    return dal.functions.authors.change_rating(request.body["ratingDiff"])
