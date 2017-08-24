from backend.entities.base_request import BaseRequest
import schema

class LectureDataRequest(BaseRequest):
    def __init__(self, raw_request_dict):
        BaseRequest.__init__(self,raw_request_dict)
        self.validate_scheme(scheme=schema.Schema({"lectureId" : str}))
        self.lecture_id = self.get_value("lectureId")

