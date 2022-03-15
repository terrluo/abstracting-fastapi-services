from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db, get_read_db
from app.schemas.foo import FooItem, FooItemCreate
from app.services.foo import FooService
from app.services.main import handle_result

router = APIRouter(
    prefix="/foo",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/item/", response_model=FooItem)
async def create_item(item: FooItemCreate, db: Session = Depends(get_db)):
    result = FooService(db).create_item(item)
    return handle_result(result)


@router.get("/item/{item_id}", response_model=FooItem)
async def get_item(item_id: int, db: Session = Depends(get_read_db)):
    result = FooService(db).get_item(item_id)
    return handle_result(result)
