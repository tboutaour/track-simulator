import abc
import numpy as np
from entities.TrackPoint_impl import TrackPoint as Point
from entities.TrackSegment_impl import TrackSegment as Segment
from entities.TrackAnalyzer_impl import TrackAnalyzer as Analyzer
import random
import geopy
import utils
NUMBER_SIMULATIONS = 4
PROB_RETURN = 0.4

class Simulator(abc.ABC):

    @abc.abstractmethod
    def simulate(self):
        """."""
        return


