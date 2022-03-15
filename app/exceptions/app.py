import typing as t

from fastapi import Request, status
from starlette.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: t.Optional[dict]):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code

        if context is None:
            context = {}

        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class AppException:
    class CreateFail(AppExceptionCase):
        def __init__(self, context: t.Optional[dict] = None):
            """
            creation failed
            """
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            AppExceptionCase.__init__(self, status_code, context)

    class NotFound(AppExceptionCase):
        def __init__(self, context: t.Optional[dict] = None):
            """
            not found
            """
            status_code = status.HTTP_404_NOT_FOUND
            AppExceptionCase.__init__(self, status_code, context)
