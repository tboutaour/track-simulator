import utils
from src.track_analyzer.interactor.analyze_track import AnalyzeTrack
from src.track_analyzer.entities.statistics import Statistics
from src.track_analyzer.repository.track_information_repository import TrackInformationRepository
from src.track_analyzer.repository.track_statistics_repository import TrackStatisticsRepository

def get_df_to_mongo(data):
    data['Point_X'] = data['Point'].map(lambda x: x.get_latitude())
    data['Point_Y'] = data['Point'].map(lambda x: x.get_longitude())
    data['Projection_X'] = data['Projection'].dropna().map(lambda x: x.get_latitude())
    data['Projection_Y'] = data['Projection'].dropna().map(lambda x: x.get_longitude())
    data = data.drop(['Point', 'Projection'], axis=1)
    return data


class AnalyzeTrackImpl(AnalyzeTrack):
    def __init__(self,
                 graph,
                 hmm,
                 id_track,
                 information_repository: TrackInformationRepository,
                 statistics_repository: TrackStatisticsRepository):
        self.graph = graph
        self.hmm = hmm
        self.statistics_repository = statistics_repository
        self.information_repository = information_repository
        self.id_track = id_track


    def analyze(self):
        self.hmm.points.pop()
        #  Realize map-matching process
        mapped_points = self.hmm.match()

        #  Complete information of mapped points into one single dataframe
        main_df = utils.join_track_projection_data(self.hmm.points, mapped_points, self.id_track)

        #  Generation of statistics information
        statistics = Statistics(self.graph, main_df)
        distance_point_projection, ac_dis_point_projection = statistics.get_distance_point_projection()
        distance_between_points, ac_dis_between_points = statistics.get_distance_between_points()

        mongo_main_df = get_df_to_mongo(main_df)

        #  Save information generated in mongoDB
        self.information_repository.write_trackinformation_dataframe(mongo_main_df)
        self.statistics_repository.write_track_statistics(self.id_track,
                                                          distance_point_projection,
                                                          list(ac_dis_point_projection))

        #  Uptdate graph information
        reduced_track = statistics.reduce_track()
        reduced_track.apply(lambda x: self.graph.update_edge_freq(x.Origin, x.Target), axis=1)

        return main_df, mapped_points
