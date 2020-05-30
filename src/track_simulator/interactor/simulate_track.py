import abc

from track_simulator.entities.track_point import TrackPoint


class SimulateTrack(abc.ABC):
    @abc.abstractmethod
    def simulate(self, origin_point: TrackPoint, distance: int):
        """
        Method to simulate track.

        :param origin_point: Node to start simulation.
        :type origin_point: TrackPoint
        :param distance: Distance of track to simulate. (in meters)
        :type distance: int
        """
        pass
