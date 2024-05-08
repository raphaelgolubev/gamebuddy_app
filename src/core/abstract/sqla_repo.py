from repository import AbastractRepository


class SQLAlchemyRepository(AbastractRepository):
    model = None

    async def add_one(self):
        pass

    async def find_all(self):
        pass
