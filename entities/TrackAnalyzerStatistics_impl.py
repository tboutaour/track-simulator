from entities.Statistics import Statistics
from entities.TrackPoint_impl import TrackPoint as Point
import pandas as pd
import numpy as np


def generate_accumulative_distribution(data):
    # Generación distribucion acumulada
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    return ser_dx


class TrackAnalyzerStatistics(Statistics):
    def __init__(self, graph, track):
        self.dataset = track
        self.graph = graph

    def get_statistics(self):
        pass

    def group_point_by_segment(self):
        grouped = pd.DataFrame({'Count': self.dataset.groupby(['Origin', 'Target']).size()})
        return grouped

    def reduce_track(self):
        return (self.dataset.loc[self.dataset.Origin.shift() != self.dataset.Origin]).reset_index(drop=True)

    def remove_noise_of_track(self):
        pass  # TODO implement method

    def get_distance_between_points(self):
        point = self.dataset['Point'].tolist()
        distance = []
        for i in range(0, len(point) - 1):
            distance.append(point[i].haversine_distance(point[i + 1]))
        return distance

    def get_distance_point_projection(self):
        self.dataset['Point_projection_distance'] = self.dataset.apply(
            lambda x: x['Point'].haversine_distance(x['Projection']), axis=1)
        self.dataset = self.dataset[self.dataset['Point_projection_distance'] < 10000]

    def normalize_dataset(data):
        list_origin_targe_reduced = list(zip(data.Origin, data.Target))
        for idx in range(0, len(list_origin_targe_reduced) - 1):
            if list_origin_targe_reduced[idx][0] == list_origin_targe_reduced[idx + 1][1]:
                aux1 = (list_origin_targe_reduced[idx][1], list_origin_targe_reduced[idx][0])
                list_origin_targe_reduced[idx] = aux1
                aux2 = (list_origin_targe_reduced[idx + 1][1], list_origin_targe_reduced[idx + 1][0])
                list_origin_targe_reduced[idx + 1] = aux2
            elif list_origin_targe_reduced[idx][1] == list_origin_targe_reduced[idx + 1][1]:
                aux2 = (list_origin_targe_reduced[idx + 1][1], list_origin_targe_reduced[idx + 1][0])
                list_origin_targe_reduced[idx + 1] = aux2
        return list_origin_targe_reduced
