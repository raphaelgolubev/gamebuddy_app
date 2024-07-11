from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abstractmethod
    def get(self, filter_by):
        raise NotImplementedError

    @abstractmethod
    def update(self, data):
        raise NotImplementedError

    @abstractmethod
    def delete(self, data):
        raise NotImplementedError
