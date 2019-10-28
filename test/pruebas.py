# -*- coding: utf-8 -*-


import TrackReader as tr
import TrackAnalyzer as ta
import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np

matplotlib.use('TkAgg')

DIRECTORY = "Rutas/Ficheros/rutasMFlores/"
SAVE_GRAPH_FILE = 'graph_file04.edgelist'
SAVE_STATISTICS_FILE = 'statistics_file04.txt'
COLOURS = ["green", "blue", "purple", "pink", "orange", "yellow", "black"]
START_NODES = [1261877527, 1261877476, 560055784]
NUMBER_REPETITIONS_ANALYZE = 1
DIRECTORY_IMAGES_ROUTES = "Imagenes/"

NORTH_CASTELL_BELLVER = 39.5713
SOUTH_CASTELL_BELLVER = 39.5573
EAST_CASTELL_BELLVER = 2.6257
WEST_CASTELL_BELLVER = 2.6023

SIGMA = 1.6
# parsed_file = tr.load_gpx_file("Rutas/Ficheros/rutasMFlores/activity_3602182164.gpx")
# track_points = tr.load_file_points(parsed_file)

track_analyzer = ta.TrackAnalyzer(NORTH_CASTELL_BELLVER, SOUTH_CASTELL_BELLVER,
                                  EAST_CASTELL_BELLVER, WEST_CASTELL_BELLVER)

nc = ['red' if node in START_NODES else 'black' for node in track_analyzer.graph.nodes]

graph = tr.load_graph_from_file(SAVE_GRAPH_FILE)
track_analyzer.compose_file_information(graph)
tr.load_track_analysis_statistics(track_analyzer, SAVE_STATISTICS_FILE)

x = np.array(range(10))

for i in range(1,20):
    y = 1/math.e**(1*x*i)
    name = "K="+str(i)
    plt.plot(x, y, label = name)
plt.legend()
plt.show()
