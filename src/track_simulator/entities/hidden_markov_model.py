import abc


class HiddenMarkovModel(abc.ABC):
    @abc.abstractmethod
    def get_emission_prob(self, projection, point):
        """
        Method to get emission probability of point-projetion relationship.
        :param projection: Point of the street network.
        :param point: Point of track without reference in street network.
        """
        pass

    @abc.abstractmethod
    def get_transition_prob(self, point, projection, next_point, next_projection):
        """
        Method to get transition probability of point and projection.
        :param point: Point of track without reference in street network.
        :param projection: Point of the street network.
        :param next_point: next Point of track, it is used to infer the probability.
        :param next_projection: Point projection of the street network of the next point.
        """
        pass

    @abc.abstractmethod
    def viterbi_algorithm(self, points):
        """
        Viterbi algorithm implementation. It uses transition and emission probabilities to detect the path related to
        a GPS point sequence.
        :param points: sequence of GPS point to analyze.
        """
        pass

