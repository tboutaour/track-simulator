# -*- coding: utf-8 -*-
"""
@author: tonibous
"""

import gpxpy
import numpy as np
import networkx as nx
import pickle

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

def save_graph_to_file(graph,path):
    # nx.write_edgelist(graph, path, data=['num of detections', 'num of points', 'frequency'])
    # with open(path, 'wb') as handle:
    #     pickle.dump(graph, handle)
    nx.write_gpickle(graph,path)

def load_graph_from_file(path):
    # G = nx.read_edgelist(path, nodetype=int, create_using=nx.MultiDiGraph,
    #                      data=(('num of detections', int), ('num of points', int), ('frequency', float),))
    G = nx.nx.read_gpickle(path)
    return G

def save_track_analysis_statistics(ta,file):
    statistics = {'trackpoint_distance': ta.trackpoint_distance, 'trackpoint_route_distance': ta.trackpoint_route_distance,
            'trackpoint_bearing': ta.trackpoint_bearing,'trackpoint_number': ta.trackpoint_number}
    with open(file, 'wb') as handle:
        pickle.dump(statistics, handle)


def load_track_analysis_statistics(ta,file):
    with open(file, 'rb') as handle:
        statistics = pickle.load(handle)
    ta.trackpoint_distance = statistics.get('trackpoint_distance')
    ta.trackpoint_route_distance = statistics.get('trackpoint_route_distance')
    ta.trackpoint_bearing = statistics.get('trackpoint_bearing')
    ta.trackpoint_number = statistics.get('trackpoint_number')