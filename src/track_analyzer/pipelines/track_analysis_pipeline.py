import os
import multiprocessing
from multiprocessing import Pool
import matplotlib.pyplot as plt
from track_analyzer.conf.config import FILE_DIRECTORY
from track_analyzer.entities.graph import Graph
from track_analyzer.repository.graph_information_repository import GraphInformationRepository
from track_analyzer.repository.track_information_repository import TrackInformationRepository
from track_analyzer.repository.track_statistics_repository import TrackStatisticsRepository
from track_analyzer.interactor.get_map_matching import GetMapMatching
from track_analyzer.interactor.get_trackanalysis_dataframe import GetTrackAnalysisDataframe
from track_analyzer.interactor.get_trackanalysis_statistics import GetTrackAnalysisStatistics
from track_analyzer.interactor.get_trackanalysis_graph import GetTrackAnalysisGraph
from track_analyzer.repository.resource.gpx_resource import GPXResource
import logging
import sys

MAX_RANGE_REPETEITION = 7


class TrackAnalysisPipeline:
    def __init__(self,
                 gpx_resource: GPXResource,
                 graph_information_repository: GraphInformationRepository,
                 track_information_repository: TrackInformationRepository,
                 track_statistics_repository: TrackStatisticsRepository,
                 get_map_matching: GetMapMatching,
                 get_track_analysis_dataframe: GetTrackAnalysisDataframe,
                 get_track_statitstics: GetTrackAnalysisStatistics,
                 get_track_graph: GetTrackAnalysisGraph,
                 graph: Graph):
        self.gpx_resource = gpx_resource
        self.graph_information_repository = graph_information_repository
        self.track_information_repository = track_information_repository
        self.track_statistics_repository = track_statistics_repository
        self.get_map_matching = get_map_matching
        self.get_track_analysis_dataframe = get_track_analysis_dataframe
        self.get_track_statistics = get_track_statitstics
        self.get_track_graph = get_track_graph
        self.graph = graph

    def run(self, file_path):
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        if file_path is None:
            file_path = FILE_DIRECTORY
        files = [gpx_file for gpx_file in os.listdir(file_path) if gpx_file.endswith(".gpx")]
        p = Pool(processes=multiprocessing.cpu_count())
        data = p.map(self.analyze, files)
        p.close()
        graphs = []
        statistics = []
        for iteration in range(1, MAX_RANGE_REPETEITION):
            #  Uptdate graph information
            graphs = [self.get_track_graph.apply(self.graph, x) for x in data]
            #  Get statistics
            statistics = [self.get_track_statistics.apply(x) for x in data]
        #################################################
        # Save statistics in MongoDB
        #################################################
        self.track_information_repository.write_trackinformation_dataframes(data=data)
        self.track_statistics_repository.write_many_track_statistics(data=statistics)
        logging.info("Saved information in MongoDB")

        self.graph_information_repository.write_graph_information_dataframe(graphs[-1].get_edgelist_dataframe())
        logging.info("Saved graph information in MongoDB")

    def analyze(self, gpx_file):
        logging.info("Analyzing: " + gpx_file)
        #################################################
        # Get points from file
        #################################################
        points = self.gpx_resource.read(FILE_DIRECTORY + '/' + gpx_file)

        #################################################
        # Map-matching of track
        #################################################
        matched_points = self.get_map_matching.match(points)
        logging.info("Analysis of " + gpx_file + " finished.")

        return self.get_track_analysis_dataframe.apply(gpx_file, points, matched_points)
