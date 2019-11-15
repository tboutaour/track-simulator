import abc

import gpxpy
import networkx as nx
import pickle


class LoaderSaver(abc.ABC):

    @abc.abstractmethod
    def loadFile(self, input):
        pass

    @abc.abstractmethod
    def parseFile(self):
        pass

    @abc.abstractmethod
    def saveFile(self, output, data):
        pass

