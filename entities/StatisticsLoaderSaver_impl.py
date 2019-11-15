from entities.LoaderSaver import LoaderSaver
import pickle

class StatisticsLoaderSaver(LoaderSaver):
    def loadFile(self, input):
        with open(input, 'rb') as handle:
            statistics = pickle.load(handle)
        ta.trackpoint_distance = statistics.get('trackpoint_distance')
        ta.trackpoint_route_distance = statistics.get('trackpoint_route_distance')
        ta.trackpoint_bearing = statistics.get('trackpoint_bearing')
        ta.trackpoint_number = statistics.get('trackpoint_number')

    def parseFile(self):
        pass

    def saveFile(self, output, data):
        statistics = {'trackpoint_distance': data.trackpoint_distance,
                      'trackpoint_route_distance': data.trackpoint_route_distance,
                      'trackpoint_bearing': data.trackpoint_bearing, 'trackpoint_number': ta.trackpoint_number}
        with open(output, 'wb') as handle:
            pickle.dump(statistics, handle)