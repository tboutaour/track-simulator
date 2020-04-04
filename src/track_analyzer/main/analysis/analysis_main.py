from track_analyzer.repository.resource.gpx_resource_impl import GPXResourceImpl
from track_analyzer.entities.graph_impl import Graph
from track_analyzer.interactor.get_map_matching_impl import GetMapMatchingImpl
from track_analyzer.pipelines.track_analysis_pipeline import TrackAnalysisPipeline
from track_analyzer.entities.hidden_markov_model_impl import HMM
from track_analyzer.main.analysis.arguments import Arguments



def analysis_main():
    args = Arguments()
    #  Resources
    gpx_resource = GPXResourceImpl()

    #  Entities
    bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)

    #  Interactors
    get_map_matching = GetMapMatchingImpl(HMM(bellver_graph))

    #  Pipeline
    track_analyzer_pipeline = TrackAnalysisPipeline(gpx_resource, get_map_matching, bellver_graph)

    #  Execution

    track_analyzer_pipeline.run(args.get_file_directory())


if __name__ == '__main__':
    analysis_main()
