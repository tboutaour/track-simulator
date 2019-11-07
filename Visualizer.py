import abc

class Visualizer(abc.ABC):

    @abc.abstractclassmethod
    def visualize(self):
        return


class GraphVisualizer(Visualizer):
    def visualize(self):
        pass

