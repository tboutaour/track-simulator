import abc

NUMBER_SIMULATIONS = 4
PROB_RETURN = 0.4

class Simulator(abc.ABC):

    @abc.abstractmethod
    def simulate(self):
        """."""
        return


