import abc


class SimulateTrack(abc.ABC):
    @abc.abstractmethod
    def simulate(self, origin_node: int, distance: int):
        """
        Method to simulate track.

        :param origin_node: Node to start simulation.
        :type origin_node: int
        :param distance: Distance of track to simulate. (in meters)
        :type distance: int
        """
        pass
