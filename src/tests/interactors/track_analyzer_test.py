import unittest
import matplotlib.pyplot as plt
from src.track_analyzer.repository.gpx_track_repository_impl import GPXTrackRepositoryImpl as LoaderSaver
from src.track_analyzer.entities.graph_impl import Graph
from src.track_analyzer.interactor.hmm_map_matching_impl import MapMatching
from src.track_analyzer.entities.hidden_markov_model_impl import HMM
from src.track_analyzer.interactor.track_analyzer_impl import TrackAnalyzerImpl
from src.track_analyzer.repository.track_information_repository_impl import TrackInformationRepositoryImpl as TrackInformationRepository
from src.track_analyzer.repository.track_statistics_repository_impl import TrackStatisticsRepositoryImpl as TrackStatisticsRepository


class MyTestCase(unittest.TestCase):
    def test_run_analysis_of_track(self):
        statistics_repository = TrackStatisticsRepository('localhost', 27019)
        information_repository = TrackInformationRepository('localhost', 27019)

        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        hidden_markov_model = HMM(graph=bellver_graph)
        fig, ax = bellver_graph.plot_graph()
        ACTIVITY = "activity_3930315984"
        FILE_PATH = "../../../tracks/Ficheros/rutasMFlores/" + ACTIVITY + ".gpx"
        test_file = LoaderSaver(FILE_PATH)  # Esto puede ir iterando
        points = list(list(zip(*test_file.parseFile()))[2])

        # Analize
        hmm = MapMatching(points, hidden_markov_model)
        analyzer = TrackAnalyzerImpl(bellver_graph, hmm, ACTIVITY, information_repository, statistics_repository)
        main_df, mapped_points = analyzer.analyze()

        # Show information
        for r in mapped_points:
            plt.scatter(r[0].get_longitude(), r[0].get_latitude(), c="red")
            print(r)
        plt.show()


if __name__ == '__main__':
    unittest.main()
