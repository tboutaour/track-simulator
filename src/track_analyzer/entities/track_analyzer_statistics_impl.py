from src.track_analyzer.entities.statistics import Statistics
import pandas as pd
import numpy as np


def generate_accumulative_distribution(data):
    # Generación distribucion acumulada
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    return ser_dx


class TrackAnalyzerStatistics(Statistics):
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
        distance = [point[i].haversine_distance(point[i + 1]) for i in range(0, len(point) - 1)]
        return distance, generate_accumulative_distribution(distance)

    def get_distance_point_projection(self):
        self.dataset['Point_projection_distance'] = self.dataset.apply(
            lambda x: x['Point'].haversine_distance(x['Projection']), axis=1)
        self.dataset = self.dataset[self.dataset['Point_projection_distance'] < 10000]
        dataset_list = list(self.dataset['Point_projection_distance'])
        return dataset_list, generate_accumulative_distribution(dataset_list)
