import typing as t

from fastapi import status

from app.exceptions.app import AppException, AppExceptionCase


class FooItemException(AppException):
    class FooItemRequiresAuth(AppExceptionCase):
        def __init__(self, context: t.Optional[dict] = None):
            """
            Item is not public and requires auth
            """
            status_code = status.HTTP_401_UNAUTHORIZED
            AppExceptionCase.__init__(self, status_code, context)
