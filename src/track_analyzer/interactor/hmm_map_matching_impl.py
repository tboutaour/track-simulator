
from src.track_analyzer.interactor.map_matching import MapMatching as dMapMatching
from src.track_analyzer.entities.hidden_markov_model import HiddenMarkovModel


class MapMatching(dMapMatching):
    def __init__(self, points, map_matching_method):
        self.points = points
        self.map_matching_method = map_matching_method

    def match(self):
        mapped_track, _ = self.map_matching_method.viterbi_algorithm(self.points)
        return mapped_track
