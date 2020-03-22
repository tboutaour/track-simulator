# -*- coding: utf-8 -*-
"""
@author: tonibous
"""
import math
import random
import geopy
import geopy.distance
import gpxpy
import gpxpy.gpx
import numpy as np
import utils
import pandas as pd
from geopy.distance import distance
from entities.TrackPoint import TrackPoint as Point
PROB_RETURN = 0.4
NUMBER_SIMULATIONS = 5
EARTH_RADIUM = 6378.1  # Radius of the Earth






