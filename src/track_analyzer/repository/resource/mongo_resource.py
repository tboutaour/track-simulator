import abc


class MongoResource(abc.ABC):

    @abc.abstractmethod
    def read(self, collection, query):
        pass

    @abc.abstractmethod
    def write(self, collection, records):
        collection.insert(records)