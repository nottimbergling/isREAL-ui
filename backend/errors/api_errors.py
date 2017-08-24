class ApiError(Exception):
    def __init__(self, side, type, description, status_code=200, extra_headers_dict=None):
        Exception.__init__(self, description)

        self.type = type
        self.description = description
        self.status_code =status_code
        self.extra_headers_dict = extra_headers_dict
        self.side = side

        self.message = self.type + "|" + self.description

    def dictify(self):
        return {"side" : self.side, "type" : self.type , "description": self.description}