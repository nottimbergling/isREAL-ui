class BaseRequest(object):
    def __init__(self, raw_request_dict):
        self.body = raw_request_dict
        if not self.body:
            self.body ={}

    def validate_scheme(self, scheme):
        scheme.validate(self.body)

    def get_value(self,key):
        return self.body[key]