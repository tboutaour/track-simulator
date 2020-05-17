
from track_simulator.interactor.get_map_matching import GetMapMatching
from track_simulator.entities.hidden_markov_model import HiddenMarkovModel


class GetMapMatchingImpl(GetMapMatching):
    def __init__(self, detection_model: HiddenMarkovModel):
        self.detection_model = detection_model

    def match(self, points):
        mapped_track, _ = self.detection_model.viterbi_algorithm(points)
        return mapped_track
