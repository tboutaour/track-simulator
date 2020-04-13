from track_analyzer.interactor.get_trackanalysis_dataframe import GetTrackAnalysisDataframe
from pandas import DataFrame
import pandas as pd


class GetTrackAnalysisDataframeImpl(GetTrackAnalysisDataframe):
    def apply(self, id_track, track, projection):
        point_df = pd.DataFrame(track, columns=['Point'])
        point_df['Point_lon'] = [point.get_longitude() for point in point_df['Point']]
        point_df['Point_lat'] = [point.get_latitude() for point in point_df['Point']]
        point_df = point_df[['Point_lat', 'Point_lon']]
        projection_df = pd.DataFrame(projection, columns=['Projection', 'Origin', 'Target'])
        projection_df['Projection_lon'] = [point.get_longitude() for point in projection_df['Projection']]
        projection_df['Projection_lat'] = [point.get_latitude() for point in projection_df['Projection']]
        projection_df = projection_df[['Projection_lat', 'Projection_lon', 'Origin', 'Target']]
        main_df = pd.concat([point_df, projection_df], axis=1)
        main_df = self.__add_dataframe_id(main_df, id_track)
        return main_df

    def __add_dataframe_id(self, data, track_id):
        data['id'] = track_id
        aux_cols = data.columns.tolist()
        aux_cols = aux_cols[-1:] + aux_cols[:-1]
        return data[aux_cols]

