import abc


class GetAnalysisFigure(abc.ABC):
    @abc.abstractmethod
    def apply_distance_point_point(self, data):
        pass

    @abc.abstractmethod
    def apply_distance_point_projection(self, data):
        pass