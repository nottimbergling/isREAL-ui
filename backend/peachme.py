import inspect
import os
import sys
from functools import wraps

import tweepy
from flask import Flask, request, redirect, url_for, session, flash
from flask import send_file

try:
    from flask_oauth import OAuth
except ImportError:
    from .flask_oauth import OAuth

from backend import config, dal, consts
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
SECRET_KEY = "development key"
app.secret_key = SECRET_KEY

oauth = OAuth()

api = None

# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
                           # unless absolute urls are used to make requests, this will be added
                           # before all URLs.  This is also true for request_token_url and others.
                           base_url='https://api.twitter.com/1.1/',
                           # where flask should look for new request tokens
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           # where flask should exchange the token with the remote application
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
                           # they mostly work the same, but for sign on /authenticate is
                           # expected because this will give the user a slightly different
                           # user interface on the twitter side.
                           authorize_url='https://api.twitter.com/oauth/authorize',
                           # the consumer keys from the twitter application registry.
                           consumer_key=consts.consumer_key,
                           consumer_secret=consts.consumer_secret
                           )


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/perform_login')
def perform_login():
    return twitter.authorize(callback=url_for('oauth_authorized',
                                              next=request.args.get('next') or request.referrer or None))


@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect("/")


def skip_if_authorized(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if session.get("screen_name"):
            return redirect("/search")
        return func(*args, *kwargs)

    return wrapped


@app.route('/authorized')
@skip_if_authorized
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('/')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['user_id'] = resp['user_id']
    session['access_key'] = resp['oauth_token']
    session['access_secret'] = resp['oauth_token_secret']
    session['screen_name'] = resp['screen_name']

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    auth = tweepy.OAuthHandler(consts.consumer_key, consts.consumer_secret)
    auth.set_access_token(session['access_key'], session['access_secret'])

    global api
    api = tweepy.API(auth)

    return redirect("/search")


@app.route('/retweet', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def retweet(request):
    # tweetId = 900804629885222913
    tweet_id = request.body.get("tweetId")
    content = request.body.get("content")
    if not validate_content(content):
        raise ValueError("Your comment appears to be inappropriate. Please review your comment."
                         "Remember, you're representing your country!")
    global api
    if not api:
        raise Exception("Not Logged in")

    screen_name = api.statuses_lookup(id_=[tweet_id, ])[0].user.screen_name
    status = api.update_status('@{username} {content}'.format(username=screen_name, content=content), tweet_id)
    dal.functions.comments.add(tweet_id, str(status.id), session["user_id"])
    return status.id


def validate_content(content):
    from profanity import profanity
    return len(content) < 100 and not profanity.contains_profanity(content)


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


@app.route('/posts/get/mine', methods=['GET'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def get_history(request):
    return dal.functions.comments.get_comments_by_user(session["user_id"])


@app.route('/posts/get/bytweet', methods=['POST'])
@response_adapter_wrapper("application/json")
@request_adapter_wrapper(BaseRequest)
def get_retweets(request):
    tweet_id = request.body.get("tweetId")
    return dal.functions.comments.get_comments_by_tweet(tweet_id)


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
    tweetid = request.body["tweetId"]
    tags = request.body["tags"]
    author_user_name = request.body["authorUserName"]
    author_display_name = request.body["authorDisplayName"]
    author_id = request.body["authorId"]
    likes = request.body["likes"]
    retweets = request.body["retweets"]
    posting_time = request.body["tweetPostingTime"]
    search_type = request.body["searchType"]

    return dal.functions.posts.add(tweetid, tags, author_display_name, author_user_name, author_id, likes, retweets,
                                   posting_time, search_type)


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
