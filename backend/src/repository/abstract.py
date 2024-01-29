from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    """
    Interface for application repositories
    """

    @abstractmethod
    def __init__(self, session):
        self.session = session

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
    def filter(self, filters: dict, foreign_keys: list = None, sub_queries: list = None):
        """
        Filters instances by passed attribute and their value

        Args:
            filters: dictionary with attributes and values
            foreign_keys: list of foreign keys fields
            sub_queries: list of fields for sub queries
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

    def delete(self, pk):
        """
        Deletes instance in storage by primary key

        Args:
            pk: primary key of the instance being deleted
        """
        raise NotImplementedError
