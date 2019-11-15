import abc


class HiddenMarkovModel(abc.ABC):
    @abc.abstractmethod
    def get_emission_prob(self, projection, point):
        pass

    @abc.abstractmethod
    def get_transition_prob(self, graph, projection, prev_point):
        pass

    @abc.abstractmethod
    def viterbi_algorithm(self,points):
        pass

    @abc.abstractmethod
    def complete_path(self, path, point):
        pass
