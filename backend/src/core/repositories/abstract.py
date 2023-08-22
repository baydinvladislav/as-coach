"""
Project repositories interface
"""

from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    """"""
    model = None

    @abstractmethod
    def create(self):
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
    def filter(self, **params):
        """"""
        raise NotImplementedError
