import os


import logging
from entities.GPXLoaderSaver_impl import GPXLoaderSaver as LoaderSaver
from entities.Graph_impl import Graph
from entities.HMMMapMatching_impl import MapMatching
from entities.HiddenMarkovModel_impl import HMM
from entities.TrackAnalyzer_impl import TrackAnalyzer
from repository.trackinformation_repository_impl import TrackInformationRepositoryImpl as TrackInformationRepository
from repository.trackstatistics_repository_impl import TrackStatisticsRepositoryImpl as TrackStatisticsRepository

FILE_DIRECTORY = "tracks/Ficheros/rutasMFlores/"







def main():
    logging.info("Main started")
    statisticsRepository = TrackStatisticsRepository('localhost', 27017)
    informationRepository = TrackInformationRepository('localhost', 27017)

    bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
    hidden_markov_model = HMM(graph=bellver_graph)
    # fig, ax = bellver_graph.plot_graph()

    id_track = 0
    for gpx_file in os.listdir(FILE_DIRECTORY):
        if gpx_file.endswith(".gpx"):
            test_file = LoaderSaver(FILE_DIRECTORY + gpx_file)  # Esto puede ir iterando
            points = list(list(zip(*test_file.parseFile()))[2])

            # Analize
            logging.warning("Analizing: " + os.path.splitext(gpx_file)[0])
            hmm = MapMatching(points, hidden_markov_model)
            analyzer = TrackAnalyzer(bellver_graph,
                                     hmm,
                                     os.path.splitext(gpx_file)[0],
                                     informationRepository,
                                     statisticsRepository)
            main_df, mapped_points = analyzer.analyze()
            logging.warning("Analysis finished")
            id_track += 1

    # Show information
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


if __name__ == '__main__':
    main()
