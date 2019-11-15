import abc


class Graph(abc.ABC):

    def get_edges(self):
        pass

    def get_nodes(self):
        pass

    def get_shortest_path(self, origin_node, target_node):
        pass

    def initialize_information(self):
        pass

    def initialize_path_frequency(self, edges):
        pass

    def update_edge_freq(self, source_node, target_node):
        pass