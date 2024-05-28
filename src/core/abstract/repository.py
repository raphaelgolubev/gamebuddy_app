from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, filter_by: dict):
        raise NotImplementedError
