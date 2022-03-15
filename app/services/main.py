import inspect
import typing as t

from loguru import logger
from sqlalchemy.orm import Session

from app.exceptions.app import AppExceptionCase

T = t.TypeVar("T")


class DBContext(t.Generic[T]):
    def __init__(self, db: T) -> None:
        self.db = db


class AppSessionService(DBContext[Session]):
    pass


class AppSessionCRUD(DBContext[Session]):
    pass


class ServiceResult:
    EXCEPTION_CLASS = AppExceptionCase

    def __init__(self, arg):
        if isinstance(arg, self.EXCEPTION_CLASS):
            self.success = False
            self.exception_case = arg.exception_case
            self.status_code = arg.status_code
        else:
            self.success = True
            self.exception_case = None
            self.status_code = None
        self.value = arg

    def __str__(self):
        if self.success:
            return "[Success]"
        return f'[Exception] "{self.exception_case}"'

    def __repr__(self):
        if self.success:
            return "<ServiceResult Success>"
        return f"<ServiceResult AppException {self.exception_case}>"

    def __enter__(self):
        return self.value

    def __exit__(self, *kwargs):
        pass


def caller_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result: ServiceResult):
    if not result.success:
        with result as exception:
            logger.error(f"{exception} | caller={caller_info()}")
            raise exception
    with result as result:
        return result
