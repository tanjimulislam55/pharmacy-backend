from typing import Any, Dict, Union
from fastapi import Request, status
from fastapi.responses import JSONResponse


def generic_exception_handler(request: Request, exception: Exception):
    print(exception)
    return JSONResponse(
        status_code=500,
        content={"context": "Something went wrong", "error": repr(exception)},
    )


class AppExceptionCase(Exception):
    def __init__(self, status_code: status, context: Union[Dict, Any]):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __repr__(self) -> str:
        return f"<Appexception {self.exception_case} - status_code={self.status_code} context={self.context}>"  # noqa E501


def app_exception_handler(request: Request, exception: AppExceptionCase):
    return JSONResponse(
        status_code=exception.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "app_exception": exception.exception_case,
            "context": exception.context,
        },
    )


class AppException(object):
    class BadRequest(AppExceptionCase):
        def __init__(self, context: dict = None):
            super().__init__(status.HTTP_400_BAD_REQUEST, context)

    class Unauthorized(AppExceptionCase):
        def __init__(self, context: dict = None):
            super().__init__(status.HTTP_401_UNAUTHORIZED, context)

    class AuthRequired(AppExceptionCase):
        def __init__(self, context: dict = None):
            super().__init__(status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED, context)

    class Forbidden(AppExceptionCase):
        def __init__(self, context: dict = None):
            super().__init__(status.HTTP_403_FORBIDDEN, context)

    class NotFound(AppExceptionCase):
        def __init__(self, context: dict = None):
            super().__init__(status.HTTP_404_NOT_FOUND, context)

    class NotAccepted(AppExceptionCase):
        def __init__(self, context: dict = None):
            super().__init__(status.HTTP_406_NOT_ACCEPTABLE, context)

    class ServerError(AppExceptionCase):
        def __init__(self, context: dict = None):
            super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, context)

    class CredentialsException(AppExceptionCase):
        def __init__(
            self, context: dict = {"message": "Could not validate credentials"}
        ):
            super().__init__(status.HTTP_400_BAD_REQUEST, context)
