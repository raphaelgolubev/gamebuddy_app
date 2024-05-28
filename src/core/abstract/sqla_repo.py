from repository import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, **data):
        pass

    async def find_all(self, **filter_by):
        pass

    async def find_one(self, **filter_by):
        pass
