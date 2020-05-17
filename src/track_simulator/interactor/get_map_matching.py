import abc

class GetMapMatching(abc.ABC):
    @abc.abstractmethod
    def match(self, points):
        pass
