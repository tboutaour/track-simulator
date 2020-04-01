import unittest
from src.track_analyzer.repository.resource.gpx_resource_impl import GPXResourceImpl
from src.track_analyzer.entities.graph_impl import Graph
from src.track_analyzer.interactor.get_map_matching_impl import GetMapMatchingImpl
from track_analyzer.pipelines.track_analysis_pipeline import TrackAnalysisPipeline
from track_analyzer.entities.hidden_markov_model_impl import HMM

FILE_DIRECTORY = "/Users/tonibous/Documents/1-UIB/TrabajoFinal/TrackAnalyzer/tracks/Ficheros/rutasMFlores/"


class MyTestCase(unittest.TestCase):
    def test_run_analysis_of_track(self):
        gpx_resource = GPXResourceImpl()
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        get_map_matching = GetMapMatchingImpl(HMM(bellver_graph))
        track_analyzer_pipeline = TrackAnalysisPipeline(gpx_resource, get_map_matching)
        fig, ax = bellver_graph.plot_graph()
        track_analyzer_pipeline.run(
            "/Users/tonibous/Documents/1-UIB/TrabajoFinal/TrackAnalyzer/tracks/Ficheros/rutasMFlores/activity_3276836874.gpx")


if __name__ == '__main__':
    unittest.main()
