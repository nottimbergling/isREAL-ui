from backend.entities.base_request import BaseRequest
import schema

class UserDataRequest(BaseRequest):
    def __init__(self, raw_request_dict):
        BaseRequest.__init__(self,raw_request_dict)
        self.validate_scheme(scheme=schema.Schema({"username" : str}))
        self.username = self.get_value("username")

