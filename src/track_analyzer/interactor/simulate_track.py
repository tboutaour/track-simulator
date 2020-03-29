import abc

NUMBER_SIMULATIONS = 4
PROB_RETURN = 0.4

class SimulateTrack(abc.ABC):

    @abc.abstractmethod
    def simulate(self):
        """."""
        return


