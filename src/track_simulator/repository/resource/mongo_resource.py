import abc


class MongoResource(abc.ABC):

    @abc.abstractmethod
    def read(self, collection, query):
        pass

    @abc.abstractmethod
    def write_graph(self, collection, graph_id, records):
        pass

    @abc.abstractmethod
    def write_statistics(self, collection, track_id, statistics_type, records):
        pass

    @abc.abstractmethod
    def write_many_statistics(self, collection, records):
        pass

    @abc.abstractmethod
    def write_track(self, collection, track_id, records):
        pass

    @abc.abstractmethod
    def write_many_track(self, collection, records):
        pass