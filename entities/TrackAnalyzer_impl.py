import utils
from entities.Analyzer import Analyzer
from entities.TrackAnalyzerStatistics_impl import TrackAnalyzerStatistics as Statistics
from repository.trackinformation_repository_impl import TrackInformationRepositoryImpl
from repository.trackstatistics_repository_impl import TrackStatisticsRepositoryImpl

def get_df_to_mongo(data):
    data['Point_X'] = data['Point'].map(lambda x: x.get_latitude())
    data['Point_Y'] = data['Point'].map(lambda x: x.get_longitude())
    data['Projection_X'] = data['Projection'].dropna().map(lambda x: x.get_latitude())
    data['Projection_Y'] = data['Projection'].dropna().map(lambda x: x.get_longitude())
    data = data.drop(['Point', 'Projection'], axis=1)
    return data


class TrackAnalyzer(Analyzer):
    def __init__(self, graph, hmm, id_track, information_repository: TrackInformationRepositoryImpl, statistics_repository: TrackStatisticsRepositoryImpl):
        self.graph = graph
        self.hmm = hmm
        self.statistics_repository = statistics_repository
        self.information_repository = information_repository
        self.id_track = id_track


    def analyze(self):
        self.hmm.points.pop()
        mapped_points = self.hmm.match()
        main_df = utils.join_track_projection_data(self.hmm.points, mapped_points, self.id_track)
        statistics = Statistics(self.graph, main_df)
        distance_point_projection, ac_dis_point_projection = statistics.get_distance_point_projection()
        distance_between_points, ac_dis_between_points = statistics.get_distance_between_points()

        mongo_main_df = get_df_to_mongo(main_df)
        self.information_repository.write_trackinformation_dataframe(mongo_main_df)
        self.statistics_repository.write_track_statistics(self.id_track,
                                                          distance_point_projection,
                                                          list(ac_dis_point_projection),
                                                          distance_between_points,
                                                          list(ac_dis_between_points))

        reduced_track = statistics.reduce_track()
        reduced_track.map(lambda x: self.graph.update_edge_freq(x['Origin'], x['Target']))

        return main_df, mapped_points
