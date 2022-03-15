from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.database import create_tables
from app.exceptions.app import AppExceptionCase, app_exception_handler
from app.exceptions.request import (
    http_exception_handler,
    request_validation_exception_handler,
)
from app.routers import foo

create_tables()

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(foo.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
