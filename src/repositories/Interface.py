from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    def create(self, data):
        raise NotImplementedError
    @abstractmethod
    def read(self, id):
        raise NotImplementedError
    @abstractmethod
    def update(self, id, data):
        raise NotImplementedError
    @abstractmethod
    def delete(self, id):
        raise NotImplementedError
