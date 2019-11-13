# -*- coding: utf-8 -*-
"""
Created on Wed May  8 17:15:18 2019
@author: tonibous
"""
from click._compat import raw_input

import TrackReader as tr
import TrackAnalyzer as ta
import TrackPlot as tp
import TrackSimulator as ts
import osmnx as ox
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

DIRECTORY = "Rutas/Ficheros/rutasMFlores/"
GPX_FILE_DIRECTORY = "Rutas/Simulaciones/"
SAVE_GRAPH_FILE = 'graph_file_prueba.edgelist'
SAVE_STATISTICS_FILE = 'statistics_file_prueba.txt'
COLOURS = ["green", "blue", "purple", "pink", "orange", "yellow", "black"]
START_NODES = [1261877527, 1261877476, 560055784]
NUMBER_REPETITIONS_ANALYZE = 1
DIRECTORY_IMAGES_ROUTES = "Imagenes/"
METHODS = {
    1: lambda: analyze_routes(),
    2: lambda: load_information(),
    3: lambda: graph_information(),
    4: lambda: simulate_route(),
    5: lambda: clear_information(),
    6: lambda: auxiliar()
}
NORTH_CASTELL_BELLVER = 39.5713
SOUTH_CASTELL_BELLVER = 39.5573
EAST_CASTELL_BELLVER = 2.6257
WEST_CASTELL_BELLVER = 2.6023

# parsed_file = tr.load_gpx_file("Rutas/Ficheros/rutasMFlores/activity_3602182164.gpx")
# track_points = tr.load_file_points(parsed_file)

track_analyzer = ta.TrackAnalyzer(NORTH_CASTELL_BELLVER, SOUTH_CASTELL_BELLVER,
                                  EAST_CASTELL_BELLVER, WEST_CASTELL_BELLVER)

nc = ['red' if node in START_NODES else 'black' for node in track_analyzer.graph.nodes]


def analyze_routes():
    files_directory = raw_input("Name of the file's directory: ")
    graph_file_name = raw_input("Name of graph file to save: ")
    statistics_file_name = raw_input("Name of statistics file to save: ")
    image_directory = raw_input("Name of directory to save images: ")
    image_directory = DIRECTORY_IMAGES_ROUTES + image_directory + '/'

    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    for l in range(0, NUMBER_REPETITIONS_ANALYZE):
        idx_col = 1
        for gpx_file in os.listdir(files_directory):
            if gpx_file.endswith(".gpx"):
                print("Analyzing: ", files_directory + gpx_file, " iter. ", l)
                parsed_file = tr.load_gpx_file(files_directory + gpx_file)
                track_points = tr.load_file_points(parsed_file)
                analyzed_track, m, simplified_route = track_analyzer.analize_track(track_points)
                track_results = np.array(analyzed_track)
                L = [(x[0], x[1], 0) for x in track_results[:, 1]]
                L_P = np.array([[x[0], x[1]] for x in track_results[:, 0]])
                track_analyzer.analyze_results(track_results)
                fig, ax = ox.plot_graph(track_analyzer.graph, fig_height=10, fig_width=10, show=False, close=False,
                                        node_color=nc)
                tp.plot_points(ax, np.array(track_points), 'blue')
                tp.plot_points(ax, np.array(simplified_route)[:, 0], 'green')
                plt.savefig(image_directory + 'Ruta' + str(idx_col) + '.png', dpi=fig.dpi)
                idx_col = idx_col + 1
                plt.close('all')
                print("Ending analysis: ", files_directory + gpx_file, " iter. ", l)
    print("Saving file in ", graph_file_name)
    tr.save_graph_to_file(track_analyzer.graph, graph_file_name)
    tr.save_track_analysis_statistics(track_analyzer, statistics_file_name)
    print("File saved.")


def load_information():
    graph_file = raw_input('File name of graph: ')
    statistics_file = raw_input('File name of statistics: ')
    print("Loading graph information from file.")
    graph = tr.load_graph_from_file(graph_file)
    track_analyzer.compose_file_information(graph)
    print("Loading statistic information from file.")
    tr.load_track_analysis_statistics(track_analyzer, statistics_file)
    print("Information loaded.")


def graph_information():
    # print("Functionability not available. Sorry.")
    tp.plot_diagrams(track_analyzer.trackpoint_bearing, "Trackpoint Bearing, meters", 100)
    tp.plot_diagrams(track_analyzer.trackpoint_distance, "Trackpoint Distance, meters", 100)
    tp.plot_diagrams(track_analyzer.trackpoint_route_distance, "Route-Track distance, meters", 100)


def clear_information():
    print("Cleaning loaded information.")
    track_analyzer = ta.TrackAnalyzer(39.5713, 39.5573, 2.6257, 2.6023)
    print("Loaded information cleaned")


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

# x = L_P[:,1]
# y = L_P[:,0]
#
# graph, = plt.plot([], [], 'o')
#
# def animate(i):
#     graph.set_data(x[:i+1], y[:i+1])
#     return graph

# ani = animation.FuncAnimation(fig, animate,frames=len(L_P), interval=200)

# tp.plot_points(ax,track_points,'black')
# tp.plot_points(ax,s[:,0],'orange')


# for i in range(0, len(track_points)):
#     ax.plot(track_points[:,0], track_points[:,1], color='black')
# plt.show()

# route = track_analyzer.create_route(s)
# ox.plot_graph_route(track_analyzer.graph, route, fig_height=10, fig_width=10)
#
# for l in L:
#      track_analyzer.update_edge_freq(l[0],l[1])

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------


# track_route_relation = track_analyzer.get_route_relation_from_trackpoint(track_points)
# track_route_relation_filtered = track_analyzer.get_simplified_route_relation(track_route_relation)
#
# originNodes = track_analyzer.get_node_points(track_route_relation_filtered[:,2])
# destinNodes = track_analyzer.get_node_points(track_route_relation_filtered[:,3])
#
# fig, ax = ox.plot_graph(track_analyzer.graph, fig_height=10, fig_width=10,
#             show=False, close=False,
#             edge_color='black')
#
# tp.plot_points(ax, track_points, 'red')
# tp.plot_points(ax, track_route_relation_filtered[:,0:2], 'blue')
#
# tp.plot_points(ax, originNodes, 'orange')
# tp.plot_points(ax,destinNodes, 'orange')
#
# tp.plot_route(track_analyzer.graph,track_route_relation_filtered)
#
# plt.show(block=True)
#
# track_analyzer.get_bearing_point_to_point(track_route_relation_filtered[:,0:2])
# track_analyzer.get_distance_point_to_point(track_route_relation_filtered[:,0:2])
#
# tp.plot_diagrams(track_analyzer.trackpoint_bearing,"Trackpoint Bearing, meters",100)
# tp.plot_diagrams(track_analyzer.trackpoint_distance,"Trackpoint Distance, meters",100)
# tp.plot_diagrams(track_analyzer.trackpoint_route_distance,"Route-Track distance, meters",100)

# frecuencies = track_analyzer.getFrequencyRoute(track_route_relation_filtered)
# track_analyzer.setFrequencyToNode(frecuencies)

def simulate_route():
    origin = 317813546
    origin = 1261877527
    end = 317813195

    # dijkstra = nx.dijkstra_path(track_analyzer.graph, origin, end, 'frequency')
    # ox.plot_graph_route(track_analyzer.graph, dijkstra, fig_height=10, fig_width=10)

    distance = int(raw_input('Distance of the route to generate (in meters): '))

    fig, ax = ox.plot_graph(track_analyzer.graph, fig_height=10, fig_width=10, show=False, close=False, node_color=nc)
    path, distance_generated = ts.simulate_route(track_analyzer, origin, end, distance, ax)
    print("Route simulated. Distance of : ", distance_generated, " meters.")
    p = np.array([[a[0], a[1]] for a in path])
    x = p[:, 1]
    y = p[:, 0]

    graph_results, = plt.plot([], [], 'o')

    def animate(i):
        graph_results.set_data(x[:i + 1], y[:i + 1])
        return graph_results

    ani = animation.FuncAnimation(fig, animate, frames=len(p), interval=100)

    tp.plot_points(ax, path, 'red')
    plt.show()
    save = raw_input('Do you want to save the simulation into .GPX file? (Y) to yes: ')
    if save.lower() == 'y':
        file_name = raw_input('name of file: ')
        file_name = GPX_FILE_DIRECTORY + file_name + '.gpx'
        ts.create_gpx_track(p,file_name)
        print("File saved.")


def auxiliar():
    ejemplo = track_analyzer.graph.edges[(302770185, 700015725,0)]
    print(ejemplo['geometry'])


option = 1
print("-----------------------------------")
print("Welcome to TrackSimulator.\n\n\n\n")
print("-----------------------------------")
while option != 0:
    print("\n\nHere are the different options right now:\n"
          "1.-Introduce real routes to analyze\n"
          "2.-Introduce information to load\n"
          "3.-Show graph information\n"
          "4.-Generate route\n"
          "5.-Clear information\n")

    option = int(raw_input('Enter an option: '))
    func = METHODS.get(option, lambda: "Invalid option")
    func()
print("\n")
print("Thank you for using this application.")
