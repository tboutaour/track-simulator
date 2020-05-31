from track_simulator.interactor.simulate_track import SimulateTrack
from track_simulator.entities.track_point import TrackPoint as Point

class TrackSimulatorPipeline:
    def __init__(self, simulate_track: SimulateTrack):
        self.simulate_track = simulate_track

    def run(self, origin_lat, origin_lon, distance, quantity):
        """
        Method to run the simulation pipeline.
        :param origin: start point of simulation.
        :param distance: distance of the track to simulate (in meters).
        :return: Simulate track in list of Point format.
        """
        if origin_lat is None or origin_lon is None:
            origin_point = Point(2.623559, 39.567875)
        else:
            origin_point = Point(origin_lon, origin_lat)
        if distance is None:
            distance = 10000
        if quantity is None:
            quantity = 1

        return [self.simulate_track.simulate(origin_point, distance) for _ in range(0, quantity)]
