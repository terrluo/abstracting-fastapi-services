import typing as t

from app.exceptions.app import AppException
from app.exceptions.foo import FooItemException
from app.models.foo import FooItem
from app.schemas.foo import FooItemCreate
from app.services.main import AppSessionCRUD, AppSessionService, ServiceResult


class FooService(AppSessionService):
    def create_item(self, item: FooItemCreate) -> ServiceResult:
        foo_item = FooCRUD(self.db).create_item(item)
        if not foo_item:
            return ServiceResult(AppException.CreateFail())
        return ServiceResult(foo_item)

    def get_item(self, item_id: int) -> ServiceResult:
        foo_item = FooCRUD(self.db).get_item(item_id)
        if not foo_item:
            return ServiceResult(AppException.NotFound({"item_id": item_id}))
        if not foo_item.public:
            return ServiceResult(FooItemException.FooItemRequiresAuth())
        return ServiceResult(foo_item)


class FooCRUD(AppSessionCRUD):
    def create_item(self, item: FooItemCreate) -> FooItem:
        foo_item = FooItem(description=item.description, public=item.public)
        self.db.add(foo_item)
        self.db.commit()
        self.db.refresh(foo_item)
        return foo_item

    def get_item(self, item_id: int) -> t.Optional[FooItem]:
        foo_item = self.db.query(FooItem).filter(FooItem.id == item_id).first()
        if foo_item:
            return foo_item
        return None
