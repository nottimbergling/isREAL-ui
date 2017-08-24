from backend.entities.base_request import BaseRequest
import schema

class SearchRequest(BaseRequest):
    def __init__(self, raw_request_dict):
        BaseRequest.__init__(self,raw_request_dict)
        self.validate_scheme(scheme=schema.Schema({"users": list, "tags": list, "freeText" : str, "username" : str}))
        self.tags = self.get_value("tags")
        self.users= self.get_value("users")
        self.free_text = self.get_value("freeText")
        self.username = self.get_value("username")

