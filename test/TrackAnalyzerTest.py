import unittest
import matplotlib.pyplot as plt
from entities.GPXLoaderSaver_impl import GPXLoaderSaver as LoaderSaver
from entities.Graph_impl import Graph
from entities.HMMMapMatching_impl import MapMatching
from entities.HiddenMarkovModel_impl import HMM
from entities.TrackAnalyzer_impl import TrackAnalyzer
from repository.trackinformation_repository_impl import TrackInformationRepositoryImpl as TrackInformationRepository
from repository.trackstatistics_repository_impl import TrackStatisticsRepositoryImpl as TrackStatisticsRepository


class MyTestCase(unittest.TestCase):
    def test_something(self):
        statistics_repository = TrackStatisticsRepository('localhost', 27017)
        information_repository = TrackInformationRepository('localhost', 27017)

        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        hidden_markov_model = HMM(graph=bellver_graph)
        fig, ax = bellver_graph.plot_graph()
        ACTIVITY = "activity_3689734814"
        FILE_PATH = "../tracks/Ficheros/rutasMFlores/" + ACTIVITY + ".gpx"
        test_file = LoaderSaver(FILE_PATH)  # Esto puede ir iterando
        points = list(list(zip(*test_file.parseFile()))[2])

        # Analize
        hmm = MapMatching(points, hidden_markov_model)
        analyzer = TrackAnalyzer(bellver_graph, hmm, ACTIVITY, information_repository, statistics_repository)
        main_df, mapped_points = analyzer.analyze()

        # Show information
        for r in mapped_points:
            plt.scatter(r[0].get_longitude(), r[0].get_latitude(), c="red")
            print(r)
        plt.show()


if __name__ == '__main__':
    unittest.main()
