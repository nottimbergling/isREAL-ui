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


@app.route('/posts/get_new', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def get_new_posts(request):
    pass


@app.route('/posts/get_hot', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def get_hot_posts(request):
    pass


@app.route('/posts/vote', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def vote(request):
    pass


@app.route('/posts/assign', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def assign(request):
    pass


@app.route('/posts/un_assign', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def un_assign(request):
    pass


@app.route('/posts/create', methods=['PUT'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def create_post(request):
    pass


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
