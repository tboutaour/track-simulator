import abc


class GetMapMatching(abc.ABC):
    @abc.abstractmethod
    def match(self, points):
        """
        This method need to implement algorithm to point detection.
        :param points: List of points to map
        """
        pass
