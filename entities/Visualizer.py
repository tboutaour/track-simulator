import abc


class Visualizer(abc.ABC):
    @abc.abstractmethod
    def visualize(self):
        pass

