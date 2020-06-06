import uuid
from datetime import datetime
import os
import utils
import matplotlib.pyplot as plt
from track_simulator.conf.config import EXPORT_SIMULATIONS_IMAGES_FOLDER
from track_simulator.repository.resource.pyplot_resource import PyplotResource

COLORS = ["green", "red", "blue", "purple", "pink", "orange", "yellow", "black"]


class PyplotResourceImpl(PyplotResource):
    def write(self, uid, graph, track):
        fig, ax = graph.plot_graph()
        utils.plot_points(ax, track, COLORS[0])
        path = utils.create_folder(EXPORT_SIMULATIONS_IMAGES_FOLDER)

        plt.savefig(path +
                    "/simulated_track_" +
                    uid +
                    ".png", format='png')
        plt.close(fig)