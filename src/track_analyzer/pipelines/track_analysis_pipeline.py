import utils
import matplotlib.pyplot as plt

from track_analyzer.interactor.get_map_matching import GetMapMatching
from track_analyzer.repository.resource.gpx_resource import GPXResource

class TrackAnalysisPipeline:
    def __init__(self,
                 gpx_resource: GPXResource,
                 get_map_matching: GetMapMatching):
        self.gpx_resource = gpx_resource
        self.get_map_matching = get_map_matching

    def run(self, file_path):
        #################################################
        # Get points from file
        #################################################
        points = self.gpx_resource.read(file_path)

        #################################################
        # Map-matching of track
        #################################################
        matched_points = self.get_map_matching.match(points)
        main_data_frame = utils.join_track_projection_data(points, matched_points, file_path)

        #################################################
        # Plotting information. (TO DEPRECATE)
        #################################################
        for index, row in main_data_frame.iterrows():
            try:
                plt.scatter(row['Point'].get_longitude(), row['Point'].get_latitude(), c="red")
                plt.scatter(row['Projection'].get_longitude(), row['Projection'].get_latitude(), c="green")
            except AttributeError:
                print("Point not found idx: " + str(index))
        plt.show()

        #################################################
        # Generate statistics of results
        #################################################
        # TODO: Implement statistics
        #################################################
        # Save statistics in MongoDB
        #################################################
        # TODO: Implement MongoDB save