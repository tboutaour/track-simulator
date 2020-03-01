import networkx
import numpy as np
import osmnx

from entities.Graph import Graph as dGraph


class Graph(dGraph):
    def __init__(self, north, south, east, west):
        self.graph = osmnx.graph_from_bbox(north, south, east, west)
        self.edge_information = self.get_edge_information_dataframe()
        self.graph_clean_and_normalize()

    def get_edges(self):
        return self.graph.edges(data=True)

    def get_edge_by_nodes(self, node_origin, node_target):
        return self.graph.edges[(node_origin, node_target, 0)]

    def get_nodes(self):
        return self.graph.nodes()

    def get_node_by_node(self, node):
        return self.graph.nodes(node)

    def get_degree(self, point):
        return self.graph.degree(point)

    def get_closest_node(self, point):
        osmnx.get_nearest_node(self.graph, point)

    def get_shortest_path_length(self, origin_node, target_node):
        try:
            shortest_path = networkx.shortest_path_length(self.graph, origin_node, target_node)
            if shortest_path > 13 and shortest_path > 0:
                shortest_path = 100000000
        except networkx.NetworkXNoPath:
            shortest_path = -1
        return shortest_path

    def get_edge_information_dataframe(self):
        df = networkx.to_pandas_edgelist(self.graph)
        del df['tunnel']
        del df['ref']
        del df['service']
        del df['lanes']
        del df['bridge']
        del df['maxspeed']
        del df['width']
        return df

    def get_shortest_path(self, origin_node, target_node):
        try:
            shortest_path = networkx.shortest_path(self.graph, origin_node, target_node)
        except networkx.NetworkXNoPath:
            shortest_path = -1
        return shortest_path

    def initialize_information(self):
        edges = list(self.graph.edges)
        ones = [1] * len(edges)
        dic_reg_ones = dict(zip(edges, ones))
        networkx.set_edge_attributes(self.graph, dic_reg_ones, 'num of detections')
        self.initialize_path_frequency(self.graph.edges)

    def initialize_path_frequency(self, edges):
        list_prob = []
        for edge in self.get_edges():
            number = len(self.graph.edges(edge[0]))
            prob = 1 / number
            list_prob.append(prob)
        dic_freq = dict(zip(edges, list_prob))
        networkx.set_edge_attributes(self.graph, dic_freq, 'frequency')

    def update_frequencies(self, edges):
        for edge in edges:
            self.update_edge_freq(edge[0], edge[1])

    def update_edge_freq(self, source_node, target_node):
        """
        Update information of edge frequency in detection. This method updates information in all edges given the source.
        This update the TrackAnalyzer object.
        :param source_node: Source node of the edge visited
        :param target_node: Target node of the edge visited
        """
        self.get_edge_by_nodes(source_node, target_node)['num of detections'] += 1
        total = sum([a[2]['num of detections'] for a in self.graph.edges(source_node, data=True)])
        for edge in self.graph.edges(source_node, data=True):
            edge[2]['frequency'] = edge[2]['num of detections']/total

    def plot_graph(self):
        fig, ax = osmnx.plot_graph(self.graph, node_color='black', node_zorder=3, show=False, close=False)
        return fig, ax

    # TODO implement graph clean
    def graph_clean_and_normalize(self):
        self.initialize_information()
        self.initialize_path_frequency(self.graph.edges)

    def get_next_node(self, node):
        node_list = [[i[1], i[2]['frequency']] for i in self.graph.get_edge_by_node(node)]
        node_list.sort(key=lambda x: x[1])
        return np.random.choice([l[0] for l in node_list], p=[l[1] for l in node_list])
