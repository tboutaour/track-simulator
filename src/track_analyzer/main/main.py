import os

import matplotlib.pyplot as plt
import logging
import numpy as np
import pandas as pd
import networkx as nx
from src.track_analyzer.repository.resource.gpx_resource_impl import GPXResourceImpl
from src.track_analyzer.entities.graph_impl import Graph
from src.track_analyzer.interactor.get_map_matching_impl import GetMapMatchingImpl
from src.track_analyzer.interactor.analyze_track_impl import AnalyzeTrackImpl
from src.track_analyzer.repository.track_information_repository_impl import TrackInformationRepositoryImpl as TrackInformationRepository
from src.track_analyzer.repository.track_statistics_repository_impl import TrackStatisticsRepositoryImpl as TrackStatisticsRepository
from src.track_analyzer.repository.graph_information_repository_impl import GraphInformationRepositoryImpl as GraphInformationRepository
from track_analyzer.pipelines.track_analysis_pipeline import TrackAnalysisPipeline
from track_analyzer.entities.hidden_markov_model_impl import HMM

FILE_DIRECTORY = "tracks/Ficheros/rutasMFlores/"


def main():
    logging.info("Main started")
    statisticsRepository = TrackStatisticsRepository('localhost', 27019)
    informationRepository = TrackInformationRepository('localhost', 27019)

    bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
    fig, ax = bellver_graph.plot_graph()

    id_track = "activity_3689734814"
    main_df = informationRepository.get_trackinformation_dataframe(id_track)
    distance_point_projection, distance_point_point = statisticsRepository.read_track_statistics()
    distance_point_projection.sort()
    cd_dx = np.linspace(0., 1., len(distance_point_projection))
    ser_dx = pd.Series(cd_dx, index=distance_point_projection)
    print("hello")

    # Show information
    for index, row in main_df.iterrows():
        plt.scatter(row['Point_Y'], row['Point_X'], c="red")
    plt.show()
    # for r in mapped_points:
    #     plt.scatter(r[0].get_longitude(), r[0].get_latitude(), c="red")
    #     print(r)
    # plt.show()

    # _, ax1 = plt.subplots()
    # plot_histogram(distance_point_projection, ax1)

    # _, ax2 = plt.subplots()
    # plot_histogram(distance_between_points, ax2)

    # plot_accumultaive_distribution(ac_dis_point_projection)
    # plot_accumultaive_distribution(ac_dis_between_points)

def main_analyze():
    logging.info("Main started")
    statisticsRepository = TrackStatisticsRepository('localhost', 27019)
    informationRepository = TrackInformationRepository('localhost', 27019)
    graphRepository = GraphInformationRepository('localhost', 27019)

    bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
    hidden_markov_model = HMM(graph=bellver_graph)
    # fig, ax = bellver_graph.plot_graph()

    id_track = 0
    for gpx_file in os.listdir(FILE_DIRECTORY):
        if gpx_file.endswith(".gpx"):
            test_file = GPXResourceImpl()  # Esto puede ir iterando
            points = list(list(zip(*test_file.parseFile()))[2])

            # Analize
            logging.warning("Analizing: " + os.path.splitext(gpx_file)[0])
            hmm = GetMapMatchingImpl(points, hidden_markov_model)
            analyzer = AnalyzeTrackImpl(bellver_graph,
                                        hmm,
                                        os.path.splitext(gpx_file)[0],
                                        informationRepository,
                                        statisticsRepository)
            main_df, mapped_points = analyzer.analyze()
            logging.warning("Analysis finished")
            id_track += 1

    graphRepository.write_graph_information_dataframe(nx.to_pandas_edgelist(bellver_graph.graph))



def main_with_analysis_pipeline():
    gpx_resource = GPXResourceImpl()
    bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
    get_map_matching = GetMapMatchingImpl(HMM(bellver_graph))
    track_analyzer_pipeline = TrackAnalysisPipeline(gpx_resource, get_map_matching)
    for gpx_file in os.listdir(FILE_DIRECTORY):
        track_analyzer_pipeline.run(FILE_DIRECTORY + gpx_file)



if __name__ == '__main__':
    main_analyze()
