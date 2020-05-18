from track_simulator.interactor.simulate_track import SimulateTrack
NUMBER_SIMULATIONS = 4


class TrackSimulatorPipeline:
    def __init__(self, simulate_track: SimulateTrack):
        self.simulate_track = simulate_track

    def run(self, origin, distance):
        """
        Method to run the simulation pipeline.
        :param origin: start node of simulation.
        :param distance: distance of the track to simulate (in meters).
        :return: Simulate track in list of Point format.
        """
        if origin is None:
            origin = 1248507104
        if distance is None:
            distance = 10000

        return self.simulate_track.simulate(origin, distance)
