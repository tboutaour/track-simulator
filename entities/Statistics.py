import abc


class Statistics(abc.ABC):
    def __init__(self, graph, track):
        self.dataset = track
        self.graph = graph

    @abc.abstractmethod
    def get_statistics(self):
        pass

    @abc.abstractmethod
    def group_point_by_segment(self):
        pass

    @abc.abstractmethod
    def reduce_track(self):
        pass

    @abc.abstractmethod
    def remove_noise_of_track(self):
        pass

    @abc.abstractmethod
    def get_distance_between_points(self):
        pass

    @abc.abstractmethod
    def get_distance_point_projection(self):
        pass

