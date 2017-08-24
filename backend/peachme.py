import inspect
import json
import sys
import json
import os
from backend import config
from backend.adapters import request_adapter
from backend.adapters.request_adapter import request_adapter_wrapper
from backend.adapters.response_adapter import response_adapter_wrapper
from backend.config import frontend_path
from backend.dal.functions.searching import get_exact_search_results, get_approximated_search_results
from backend.dal.mongo_client.mongodb_client import _recursive_convert_object_id_to_string
from backend.entities.base_request import BaseRequest
from backend.entities.lecture_data_request import LectureDataRequest
from backend.entities.search_request import SearchRequest
from flask import Flask, send_file, request, Response, redirect
from backend.entities.update_lecture_data_request import UpdateLectureDataRequest
from backend.entities.user_data_request import UserDataRequest
from backend.logs.logger import logger
from backend.dal.functions.spaces_and_instances import get_all_spaces
from backend.dal.functions.lectures_and_users import *
from backend.entities.base_request import BaseRequest
from backend.entities.user_insert_request import InsertUser, InsertLecture, InsertTag
from bson.objectid import ObjectId
from backend.dal.functions import lectures_and_users

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


@app.route('/update_user_data', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(UpdateLectureDataRequest)
def update_user_data(request):
    pass