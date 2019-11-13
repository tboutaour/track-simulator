import networkx


class Graph(networkx.classes.DiGraph):
    def __init__(self, g: networkx.DiGraph):
        self.graph = g

    def get_edges(self):
        return self.graph.edges(data=True)

    def get_nodes(self):
        return self.graph.nodes()

    def get_shortest_path(self, origin_node, target_node):
        try:
            shortest_path = networkx.shortest_path(self.graph, origin_node, target_node)
        except networkx.NetworkXNoPath:
            shortest_path = 100
        return shortest_path

    def initialize_information(self):
        edges = list(self.graph.edges)
        zeros = [0] * len(edges)
        ones = [1] * len(edges)
        dic_reg_zeros = dict(zip(edges, zeros))
        dic_reg_ones = dict(zip(edges, ones))
        networkx.set_edge_attributes(self.graph, dic_reg_ones, 'num of detections')
        networkx.set_edge_attributes(self.graph, dic_reg_zeros, 'num of points')
        self.initialize_path_frequency()

    def initialize_path_frequency(self, edges):
        list_prob = []
        for edge in self.get_edges():
            number = len(self.graph.edges(edge[0]))
            prob = 1 / number
            list_prob.append(prob)
        dic_freq = dict(zip(edges, list_prob))
        networkx.set_edge_attributes(self.graph, dic_freq, 'frequency')

    def update_edge_freq(self, source_node, target_node):
        """
        Update information of edge frequency in detection. This method updates information in all edges given the source.
        This update the TrackAnalyzer object.
        :param source_node: Source node of the edge visited
        :param target_node: Target node of the edge visited
        """
        self.graph.edges[(source_node, target_node, 0)]['num of detections'] += 1
        total = self.df['num of detections'][self.df['source'] == source_node].sum()
        for edge in self.graph.edges(source_node):
            self.graph.edges[(edge[0],edge[1],0)]['frequency'] = self.graph.edges[(edge[0],edge[1],0)][ 'num of detections']/total
##        self.df = networkx.to_pandas_edgelist(self.graph, source='source', target='target')

