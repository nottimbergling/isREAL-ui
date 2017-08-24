from backend.errors.api_errors import ApiError


class BadFormatError(ApiError):
    def __init__(self, description="request was not well formatted"):
        ApiError.__init__(self, "server", "Bad Format", description)


