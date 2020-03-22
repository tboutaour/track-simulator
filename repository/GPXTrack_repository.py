import abc


class GPXTrackRepository(abc.ABC):

    def loadFile(self):
        pass

    def parseFile(self):
        pass

    def saveFile(self, output, data):
        pass