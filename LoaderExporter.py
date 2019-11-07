import abc


class LoaderSaver(abc.ABC):

    @abc.abstractmethod
    def loadFile(self, input):
        """Retrieve data from the input source and return an object."""
        return

    @abc.abstractmethod
    def parseFile(self):
        """Retrieve data from the file source and return an iterator."""
        return

    @abc.abstractmethod
    def saveFile(self, output, data):
        """Retrieve data from the input source and return an object."""
        return


class GraphLoaderSaver(LoaderSaver):
    def loadFile(self, input):
        pass

    def parseFile(self):
        pass

    def saveFile(self, output, data):
        pass


class StatisticsLoaderSaver(LoaderSaver):
    def loadFile(self, input):
        pass

    def parseFile(self):
        pass

    def saveFile(self, output, data):
        pass


class GPXLoaderSaver(LoaderSaver):
    def loadFile(self, input):
        pass

    def parseFile(self):
        pass

    def saveFile(self, output, data):
        pass
