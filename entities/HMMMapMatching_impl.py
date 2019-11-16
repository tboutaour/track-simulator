from entities.MapMatching import MapMatching as dMapMatching
from entities.HiddenMarkovModel_impl import HMM
from entities.TrackPoint_impl import TrackPoint as Point


class MapMatching(dMapMatching):
    def __init__(self, points: Point, hmm: [HMM]):
        self.points = points
        self.hmm = hmm

    def match(self):
        self.hmm.viterbi_algorithm(self.points)
