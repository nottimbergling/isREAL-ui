from backend.errors.api_errors import ApiError


class UnexpectedError(ApiError):
    def __init__(self, inner_error):
        self.inner_error =inner_error
        ApiError.__init__(self, "server", "Unexcpected", str(inner_error))


    def dictify(self):
        jstr = ApiError.dictify(self)
        jstr["innerType"] = str(type(self.inner_error))
        return jstr