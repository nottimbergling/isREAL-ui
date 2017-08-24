import json

from backend.entities.peach_response import PeachResponse
from backend.errors.api_errors import ApiError
from backend.errors.unexpected_error import UnexpectedError
from functools import wraps

from flask import Response


def response_adapter_wrapper(mimetype="text/plain"):
    def func_wrapper(func):
        @wraps(func)
        def wrapper(**params):

            try:
                func_result = func(**params)
                if type(func_result) is Response:
                    return func_result

                response = PeachResponse(func_result)

            except ApiError as err:
                response = PeachResponse(err.dictify(),"error", err.status_code, err.extra_headers_dict)

            except Exception as error:
                err = UnexpectedError(error)
                response = PeachResponse(err.dictify(),"error", err.status_code, err.extra_headers_dict)

            return _make_http_response(response.dictify(),response.http_status_code,response.http_extra_headers,mimetype)
        return wrapper
    return func_wrapper



def _make_http_response(content=None, status_code=200, extra_headers=None, mimetype="text/plain"):

    extra_headers= extra_headers or {}
    extra_headers["Access-Control-Allow-Origin"] = "http://localhost:8000/*"
    if content is None:
        content_string = ""
        mimetype = "text/plain"
    else:
        if mimetype == "application/json":
            content_string = json.dumps(content)
        else:
            content_string =content

    return Response(content_string,status_code,extra_headers,mimetype)

