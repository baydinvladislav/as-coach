"""
Project repositories interface
"""

from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    """"""

    @abstractmethod
    def create(self, **params):
        """"""
        raise NotImplementedError

    @abstractmethod
    def get(self, pk):
        """"""
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        """"""
        raise NotImplementedError

    @abstractmethod
    def filter(self, attribute, value):
        """"""
        raise NotImplementedError

    def update(self, pk, **params):
        """"""
        raise NotImplementedError

    # def delete(self, pk, **params):
    #     """"""
    #     raise NotImplementedError
