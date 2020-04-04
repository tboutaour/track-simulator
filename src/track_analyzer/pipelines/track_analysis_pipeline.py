import os
import matplotlib.pyplot as plt
import utils
from track_analyzer.conf.config import FILE_DIRECTORY
from track_analyzer.entities.graph import Graph
from track_analyzer.interactor.get_map_matching import GetMapMatching
from track_analyzer.repository.resource.gpx_resource import GPXResource


class TrackAnalysisPipeline:
    def __init__(self,
                 gpx_resource: GPXResource,
                 get_map_matching: GetMapMatching,
                 graph: Graph):
        self.gpx_resource = gpx_resource
        self.get_map_matching = get_map_matching
        self.graph = graph

    def run(self, file_path):
        import logging
        import sys
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        if file_path is None:
            file_path = FILE_DIRECTORY
        logging.info("Main started.")
        for gpx_file in os.listdir(file_path):
            if gpx_file.endswith(".gpx"):
                logging.info("Analyzing: " + gpx_file)
                #################################################
                # Get points from file
                #################################################
                points = self.gpx_resource.read(FILE_DIRECTORY + '/' + gpx_file)

                #################################################
                # Map-matching of track
                #################################################
                matched_points = self.get_map_matching.match(points)
                main_data_frame = utils.join_track_projection_data(points, matched_points, gpx_file)

                logging.info("Analysis of " + gpx_file + " finished.")
                fig, ax = self.graph.plot_graph()
                #################################################
                # Plotting information. (TO DEPRECATE)
                #################################################
                for index, row in main_data_frame.iterrows():
                    try:
                        plt.scatter(row['Point'].get_longitude(), row['Point'].get_latitude(), c="red")
                        plt.scatter(row['Projection'].get_longitude(), row['Projection'].get_latitude(), c="green")
                    except AttributeError:
                        print("Point not found idx: " + str(index))
                #################################################
                # Generate statistics of results
                #################################################
                # TODO: Implement statistics
                #################################################
                # Save statistics in MongoDB
                #################################################
                # TODO: Implement MongoDB save

                # #  Save information generated in mongoDB
                # self.information_repository.write_trackinformation_dataframe(mongo_main_df)
                # self.statistics_repository.write_track_statistics(self.id_track,
                #                                                   distance_point_projection,
                #                                                   list(ac_dis_point_projection))
                #
                # #  Uptdate graph information
                # reduced_track = statistics.reduce_track()
                # reduced_track.apply(lambda x: self.graph.update_edge_freq(x.Origin, x.Target), axis=1)

        plt.show()
