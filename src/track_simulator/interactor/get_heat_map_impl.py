from track_simulator.interactor.get_heat_map import GetHeatMap
from track_simulator.entities.graph_impl import Graph
import matplotlib.cm as cm
import osmnx
import matplotlib.colors as colors


class GetHeatMapImpl(GetHeatMap):
    def apply(self, graph: Graph, data):
        ev = [edge[2]['num of detections'] for edge in graph.get_edges()]
        norm = colors.Normalize(vmin=min(ev) * 0.8, vmax=max(ev))
        cmap = cm.ScalarMappable(norm=norm, cmap=cm.inferno)
        ec = [cmap.to_rgba(cl) for cl in ev]
        fig, ax = osmnx.plot_graph(graph.graph,
                                   bgcolor='k',
                                   node_color='black',
                                   edge_color=ec,
                                   edge_linewidth=1.5,
                                   edge_alpha=1)

    def __get_node_colors_by_stat(self, data, criteria):
        df = data.sort_values(criteria)
        df['colors'] = self.__get_color_list(df)
        return df

    def __get_color_list(self, df):
        return osmnx.get_colors(n=len(df), cmap='inferno', start=0.2)
