import abc


class GetAnalysisFigure(abc.ABC):
    @abc.abstractmethod
    def apply_distance_point_point(self, data):
        """
        Definition of method to get point to point figure.

        :param data: List of distances point to point.
        """
        pass

    @abc.abstractmethod
    def apply_distance_point_projection(self, data):
        """
        Definition of method to get distance point to projection figure.

        :param data: List of distances point to projection.
        """
        pass
