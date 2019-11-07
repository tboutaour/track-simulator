import abc


class Simulator(abc.ABC):

    @abc.abstractmethod
    def simulate(self):
        """."""
        return


class TrackSimulator(Simulator):

    def simulate(self):
        pass
