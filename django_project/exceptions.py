from typing import Optional

from rest_framework.exceptions import APIException


class BaseRequestException(APIException):
    status_code: int

    def __init__(self, message: Optional[str] = None, code: Optional[str] = None, data: Optional[dict] = None):
        detail = None
        if data:
            detail = data
        elif message and code:
            detail = {'message': message, 'code': code}

        super().__init__(detail)


class BadRequestException(BaseRequestException):
    status_code = 400
