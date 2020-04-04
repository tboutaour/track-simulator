import abc


class SimulateTrack(abc.ABC):
    @abc.abstractmethod
    def simulate(self, origin_node, distance):
        pass
