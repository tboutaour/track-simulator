from entities.Statistics import Statistics
from entities.TrackPoint_impl import TrackPoint as Point
import pandas as pd


class TrackAnalyzerStatistics(Statistics):
    def __init__(self, graph, track):
        self.dataset = pd.DataFrame(track,
                                    columns=['X_point', 'Y_point', 'X_projection', 'Y_projection', 'Origin', 'Target'])
        self.graph = graph
        self.track = track

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
        point_x = self.dataset['X_point'].tolist()
        point_y = self.dataset['Y_point'].tolist()
        distance = []
        for i in range(0, len(point_x) - 1):
            distance.append(Point(point_x[i], point_y[i]).distance(Point(point_x[i + 1], point_y[i + 1])))
        return distance

    def get_distance_point_projection(self):
        self.dataset['Point_projection_distance'] = self.dataset.apply(
            lambda row: Point(row.X_point, row.Y_point).distance(Point(row.X_projection, row.Y_projection)), axis=1)

