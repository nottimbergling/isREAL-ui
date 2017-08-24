import schema

from backend.entities.base_request import BaseRequest


class SearchRequest(BaseRequest):
    def __init__(self, raw_request_dict):
        BaseRequest.__init__(self, raw_request_dict)
        self.validate_scheme(scheme=schema.Schema({"authors": list, "tags": list, "maxResults": int}))
        self.tags = self.get_value("tags")
        self.users = self.get_value("authors")
        self.maxResults = self.get_value("maxResults")
