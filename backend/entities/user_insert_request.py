from backend.entities.base_request import BaseRequest
from backend.dal.functions import dal_config
import schema

class InsertUser(BaseRequest):
    def __init__(self, raw_request_dict):
        BaseRequest.__init__(self,raw_request_dict)
        self.scheme = schema.Schema({
            dal_config.USERS_COLLECTION_USERNAME_KEY: str,
            dal_config.USERS_COLLECTION_DISPLAY_NAME_KEY: str,
            dal_config.USERS_COLLECTION_TAGS_KEY: list,
            dal_config.USERS_COLLECTION_CONTACT_DETAILS_KEY: dict,
            dal_config.USERS_COLLECTION_AVAILABILITY_KEY: dict
            })
        self.validate_scheme(scheme=self.scheme)


class InsertLecture(BaseRequest):
    def __init__(self, raw_request_dict):
        BaseRequest.__init__(self,raw_request_dict)
        self.scheme = schema.Schema({
            dal_config.LECTURES_COLLECTION_USERNAME_KEY: str,
            dal_config.LECTURES_COLLECTION_TITLE_KEY: str,
            dal_config.LECTURES_COLLECTION_DESCRIPTION_KEY: str,
            dal_config.LECTURES_COLLECTION_RATING_KEY: list,
            dal_config.LECTURES_COLLECTION_TAGS_KEY: list,
            dal_config.LECTURES_COLLECTION_COMMENTS_KEY: list
            })
        self.validate_scheme(scheme=self.scheme)

class InsertTag(BaseRequest):
    def __init__(self, raw_request_dict):
        BaseRequest.__init__(self,raw_request_dict)
        self.scheme = schema.Schema({
            dal_config.USERS_COLLECTION_USERNAME_KEY: str,
            dal_config.TAGS_COLLECTION_NAME_KEY: str
            })
        self.validate_scheme(scheme=self.scheme)

        