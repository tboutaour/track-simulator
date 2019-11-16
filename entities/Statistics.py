import abc


class Statistics(abc.ABC):
    @abc.abstractmethod
    def get_statistics(self):
        pass
