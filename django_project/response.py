from rest_framework.response import Response


class BaseResponse(Response):
    status_code: int

    def __init__(self, data: dict = None, message: str = None, code: str = None):
        if data:
            self._data = data
        elif message and code:
            self._data = {'message': message, 'code': code}
        else:
            self._data = None

        super().__init__(self._data)


class AccessResponse(BaseResponse):
    status_code = 200


class BadResponse(BaseResponse):
    status_code = 400


class ForbiddenResponse(BaseResponse):
    status_code = 403
