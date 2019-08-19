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
SAVE_GRAPH_FILE = 'graph_file.edgelist'
SAVE_STATISTICS_FILE = 'statistics_file.txt'
COLOURS = ["green", "blue", "purple", "pink", "orange", "yellow", "black"]
START_NODES = [1261877527,1261877476,560055784]
METHODS = {
    1: lambda: analyze_routes(),
    2: lambda: load_information(),
    3: lambda: simulate_route()
}
# parsed_file = tr.load_gpx_file("Rutas/Ficheros/rutasMFlores/activity_3602182164.gpx")
# track_points = tr.load_file_points(parsed_file)

track_analyzer = ta.TrackAnalyzer(39.5713,39.5573,2.6257,2.6023)
track_analyzer.set_kdtree()

nc = ['red' if node in START_NODES else 'black' for node in track_analyzer.graph.nodes]


def analyze_routes():
    for l in range(0,10):
        idx_col = 0
        for gpx_file in os.listdir("Rutas/Ficheros/rutasMFlores/"):
            if gpx_file.endswith(".gpx"):
                print("Analizando: ",DIRECTORY+gpx_file," iteración ",l)
                parsed_file = tr.load_gpx_file(DIRECTORY+gpx_file)
                track_points = tr.load_file_points(parsed_file)
                analyzed_track, m, simplified_route = track_analyzer.analize_track(track_points)
                track_results = np.array(analyzed_track)
                L = [(x[0],x[1],0) for x in track_results[:,1]]
                L_P = np.array([[x[0],x[1]] for x in track_results[:,0]])
                track_analyzer.analyze_results(track_results)
                # tp.plot_points(ax,s[:,0],COLOURS[idx_col % len(COLOURS)])
                # idx_col = idx_col + 1
                print("Finalizando análisis: ", DIRECTORY + gpx_file," iteración ",l)
    print("Guardando el fichero de almacenamiento en ",SAVE_GRAPH_FILE)
    tr.save_graph_to_file(track_analyzer.graph,SAVE_GRAPH_FILE)
    tr.save_track_analysis_statistics(track_analyzer,SAVE_STATISTICS_FILE)
    print("Fichero guardado.")


def load_information():
    graph_file = raw_input('File name of Graph: ')
    statistics_file = raw_input('File name of statistics: ')
    print("Cargando archivo de información de grafo")
    graph = tr.load_graph_from_file(SAVE_GRAPH_FILE)
    track_analyzer.compose_file_information(graph)
    print("Cargando archivo de información de estadísticas")
    tr.load_track_analysis_statistics(track_analyzer,SAVE_STATISTICS_FILE)
    print("Cargado correcto")
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------


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
    path,distance_generated = ts.simulate_route(track_analyzer, origin, end, distance, ax)

    p = np.array([[a[0],a[1]] for a in path])
    x = p[:,1]
    y = p[:,0]

    graph_results, = plt.plot([], [], 'o')

    def animate(i):
        graph_results.set_data(x[:i + 1], y[:i + 1])
        return graph_results

    ani = animation.FuncAnimation(fig, animate,frames=len(p), interval=100)

    tp.plot_points(ax, path, 'red')
    plt.show()



option = 1
print("-----------------------------------")
print("Welcome to TrackSimulator.\n\n\n\n")
print("-----------------------------------")
while option != 0:
    print("\n\nHere are the different options right now:\n"
          "1.-Introduce real routes to analyze\n"
          "2.-Introduce information to load\n"
          "3.-Generate route\n")

    option = int(raw_input('Enter an option: '))
    func = METHODS.get(option, lambda: "Invalid option")
    func()
print("\n")
print("Thank you for using this application.")