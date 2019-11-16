import abc


class MapMatching(abc.ABC):
    @abc.abstractmethod
    def match(self):
        pass
