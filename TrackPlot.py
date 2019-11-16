# -*- coding: utf-8 -*-
"""
@author: tonibous
"""
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import numpy as np
import pandas as pd


def plot_points(ax, t, color):
    [ax.scatter(lon, lat, c = 'red', s=20) for lat,lon in t]

def plot_route(graph, track):
    routes = []
    for i in track:
        routes.append(nx.shortest_path(graph, i[2], i[3], weight='length'))
    ox.plot_graph_routes(graph, routes, route_linewidth=1, orig_dest_node_size=3)

def get_frequency(data,title):
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    fig, ax = plt.subplots()
    ax = ser_dx.plot(drawstyle='steps', legend="True")
    ax.set_xlabel(title, fontsize=16)
    ax.set_ylabel("Frequency", fontsize=16)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    ax.legend().set_visible(False)
    ax.grid(True)
    fig.canvas.draw()

def get_histogram(data,title,bins):
    fig, ax = plt.subplots()
    plt.hist(data, bins=bins)
    ax.set_xlabel(title, fontsize=16)
    ax.set_ylabel("Frequency", fontsize=16)
    ax.grid(True)
    fig.canvas.draw()

def plot_diagrams(data,title,bins):
    get_histogram(data,title,bins)
    plt.show()
    get_frequency(data, title)
    plt.show()