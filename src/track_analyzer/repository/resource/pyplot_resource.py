import abc

class PyplotResource(abc.ABC):
    @abc.abstractmethod
    def write(self, uid, graph, track):
        pass