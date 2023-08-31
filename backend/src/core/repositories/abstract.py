"""
Project repositories interface
"""

from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    """
    Interface for application repositories
    """

    @abstractmethod
    def create(self, **params):
        """
        Creates instance in storage
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, pk):
        """
        Gets instance from storage by primary key

        Args:
            pk: primary key of the instance being updated
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        """
        Gets all instance from table storage
        """
        raise NotImplementedError

    @abstractmethod
    def filter(self, attribute, value):
        """
        Filters instances by passed attribute and their value

        Args:
            attribute: name of instance attribute
            value: attribute's value
        """
        raise NotImplementedError

    def update(self, pk, **params):
        """
        Updates instance in storage by primary key

        Args:
            pk: primary key of the instance being updated
            params: parameters for instance updating
        """
        raise NotImplementedError

    # TODO: implement soft deletion
    # def delete(self, pk, **params):
    #     """"""
    #     raise NotImplementedError
