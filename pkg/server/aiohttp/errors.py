class ApiError(Exception):
    def __init__(self, message):
        super().__init__(message)

    code = 500


class ErrNotFount(ApiError):
    code = 404


class ClientError(ApiError):
    code = 400


class ErrAlreadyExist(ClientError):
    ...


class ErrForbidden(ClientError):
    ...


class AuthError(ApiError):
    code = 401


class ErrUnauthorized(AuthError):
    ...
