
from interactor.MapMatching import MapMatching as dMapMatching
from entities.HiddenMarkovModel import HiddenMarkovModel


class MapMatching(dMapMatching):
    def __init__(self, points, hmm: [HiddenMarkovModel]):
        self.points = points
        self.hmm = hmm

    def match(self):
        mapped_track, _ = self.hmm.viterbi_algorithm(self.points)
        return mapped_track
