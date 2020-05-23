import abc


class SimulateTrack(abc.ABC):
    @abc.abstractmethod
    def simulate(self, origin_node, distance):
        """
        Method to simulate track.

        :param origin_node: Node to start simulation.
        :param distance: Distance of track to simulate. (in meters)
        """
        pass
