import abc


class Graph(abc.ABC):

    def get_edges(self):
        pass

    def get_edge_by_nodes(self, node_origin, node_target):
        pass

    def get_edge_by_node(self, node_origin):
        pass

    def get_nodes(self):
        pass

    def get_node_by_node(self, node):
        pass

    def get_degree(self, point):
        pass

    def get_closest_node(self, point):
        pass

    def load_graph_analysis_statistics(self, data):
        pass


    def get_shortest_path_length(self, origin_node, target_node):
        pass

    def get_edge_information_dataframe(self):
        pass

    def get_shortest_path(self, origin_node, target_node):
        pass

    def initialize_information(self):
        pass

    def initialize_path_frequency(self, edges):
        pass

    def update_frequencies(self, edges):
        pass

    def update_edge_freq(self, source_node, target_node):
        pass

    def plot_graph(self):
        pass

    def graph_clean_and_normalize(self):
        pass

    def complete_graph(self):
        pass

    def get_next_node(self, node):
        pass

    def get_edgelist_dataframe(self):
        pass