import base64

from backend.errors.bad_foramt_error import BadFormatError
from functools import wraps
from flask import request, redirect, url_for


def extract_username():
    username = request.headers.get("Authorization")
    if "Basic" == username[:5]:
        username = username[6:]
        username = base64.b64decode(username).decode("utf-8")
        username, password = str(username).split(':')
    return username


def request_adapter_wrapper(entity):
    def actual_decorator(api_func):
        @wraps(api_func)
        def wrapper(**params):
            try:
                raw_request = request.json
            except:
                raise BadFormatError("request data was not a valid json")

            request_obj = entity(raw_request, **params)

            params["request"] = request_obj

            response = api_func(**params)

            return response

        return wrapper

    return actual_decorator
