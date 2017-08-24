from backend.entities.base_request import BaseRequest
import schema

class UpdateLectureDataRequest(BaseRequest):
    def __init__(self, raw_request_dict):
        BaseRequest.__init__(self,raw_request_dict)
        self.lecture_id = self.body.get("lectureId",None)
        self.username = self.body.get("username", None)
        self.tags = self.body.get("tags", None)
        self.description = self.body.get("description", None)
        self.title = self.body.get("title", None)
        self.category =self.body.get("category",None)

