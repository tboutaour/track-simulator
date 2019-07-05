# -*- coding: utf-8 -*-
"""
@author: tonibous
"""

import gpxpy
import numpy as np

def load_gpx_file(file):
    local_file = open(file)
    parsed_file = gpxpy.parse(local_file)
    return parsed_file

def load_file_points(file):
    points_a = []
    for track in file.tracks:  # OJO SOLO HAY UN TRACK
        for segment in track.segments:  # OJO SOLO HAY UN SEGMENT
            for iA in range(0, len(segment.points) - 1):
                point = segment.points[iA]
                points_a.append([point.latitude, point.longitude])
    return np.array(points_a)

