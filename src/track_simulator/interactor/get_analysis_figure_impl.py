from track_simulator.interactor.get_analysis_figure import GetAnalysisFigure
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import osmnx
import matplotlib.colors as colors
import matplotlib.cm as cm
from track_simulator.conf.config import EXPORT_ANALYSIS_IMAGES_FOLDER


class GetAnalysisFigureImpl(GetAnalysisFigure):
    def apply_distance_point_point(self, data):
        ser_dx, net_dx2 = self.__generate_cumulative_distribution(data, 40)

        plt.figure(figsize=(7, 8))
        # Plot Cummulative distribution
        plt.subplot(211)
        ser_dx.plot(drawstyle='default', legend="True")
        plt.xlabel("Meters")
        plt.ylabel("Frequency")
        plt.title("Cumulative distribution of distance point to point")
        plt.legend().set_visible(False)
        plt.grid(True)

        # Plot Histogram
        plt.subplot(212)
        plt.hist(net_dx2, bins=300, alpha=0.5)
        plt.xlabel('Distance point to point')
        plt.ylabel('Frequency')
        plt.title('Histogram of distance point to point')
        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                            wspace=0.35)
        today = datetime.utcnow()
        str_day = today.strftime('%Y%m%d_%H%M') + "00"
        plt.savefig(EXPORT_ANALYSIS_IMAGES_FOLDER + '/' + 'distance_point_point_' + str_day + '.png', format='png',
                    dpi=600)

    def apply_distance_point_projection(self, data):
        ser_dx, net_dx2 = self.__generate_cumulative_distribution(data, 40)

        # Plot Cummulative distribution
        plt.figure(figsize=(7, 8))
        plt.subplot(211)
        ser_dx.plot(drawstyle='default', legend="True", color='green')
        plt.xlabel("Meters")
        plt.ylabel("Frequency")
        plt.title("Cumulative distribution of distance point to projection")
        plt.legend().set_visible(False)
        plt.grid(True)

        # Plot Histogram
        plt.subplot(212)
        plt.hist(net_dx2, bins=300, alpha=0.5, color='green')
        plt.xlabel('Distance point to point')
        plt.ylabel('Frequency')
        plt.title('Histogram of distance point to projection')
        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                            wspace=0.35)
        today = datetime.utcnow()
        str_day = today.strftime('%Y%m%d_%H%M') + "00"
        plt.savefig(EXPORT_ANALYSIS_IMAGES_FOLDER + '/' + 'distance_point_projection_' + str_day + '.eps', format='eps',
                    dpi=600)

    def apply_heat_map(self, graph):
        ev = [edge[2]['num of detections'] for edge in graph.get_edges()]
        norm = colors.Normalize(vmin=min(ev) * 0.8, vmax=max(ev))
        cmap = cm.ScalarMappable(norm=norm, cmap=cm.inferno)
        ec = [cmap.to_rgba(cl) for cl in ev]
        today = datetime.utcnow()
        str_day = today.strftime('%Y%m%d_%H%M') + "00"
        osmnx.plot_graph(graph.graph,
                         save=True,
                         show=False,
                         close=False,
                         file_format='png',
                         filename=EXPORT_ANALYSIS_IMAGES_FOLDER + '/' + 'heat_map_' + str_day,
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

    def __generate_cumulative_distribution(self, data, threshold):
        data.sort()
        net_dx2 = [i for i in data if i < threshold]
        net_dx2 = np.array(net_dx2)
        net_dx2 = np.sort(net_dx2)
        cd_dx = np.linspace(0., 1., len(net_dx2))
        return pd.Series(cd_dx, index=net_dx2), net_dx2
