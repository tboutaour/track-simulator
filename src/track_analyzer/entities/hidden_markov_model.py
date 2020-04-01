import abc


class HiddenMarkovModel(abc.ABC):
    @abc.abstractmethod
    def get_emission_prob(self, projection, point):
        pass

    @abc.abstractmethod
    def get_transition_prob(self, point, projection, next_point, next_projection):
        pass

    @abc.abstractmethod
    def viterbi_algorithm(self, points):
        pass

