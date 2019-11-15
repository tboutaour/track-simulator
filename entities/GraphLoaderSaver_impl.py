from entities.LoaderSaver import LoaderSaver
import osmnx as nx

class GraphLoaderSaver(LoaderSaver):
    def loadFile(self, input):
        # G = nx.read_edgelist(path, nodetype=int, create_using=nx.MultiDiGraph,
        #                      data=(('num of detections', int), ('num of points', int), ('frequency', float),))
        G = nx.read_gpickle(input)
        return G

    def parseFile(self):
        pass

    def saveFile(self, output, data):
        nx.write_gpickle(data, output)