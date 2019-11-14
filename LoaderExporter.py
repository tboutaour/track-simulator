import abc

import gpxpy
import networkx as nx
import pickle


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
        # G = nx.read_edgelist(path, nodetype=int, create_using=nx.MultiDiGraph,
        #                      data=(('num of detections', int), ('num of points', int), ('frequency', float),))
        G = nx.read_gpickle(input)
        return G

    def parseFile(self):
        pass

    def saveFile(self, output, data):
        nx.write_gpickle(data, output)


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


class GPXLoaderSaver(LoaderSaver):
    def loadFile(self, input):
        local_file = open(input)
        parsed_file = gpxpy.parse(local_file)
        return parsed_file

    def parseFile(self):
        pass

    def saveFile(self, output, data):
        pass

    def create_gpx_track(data, file_name):
        # Creating a new file:
        gpx = gpxpy.gpx.GPX()

        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        # Create points:
        [gpx_segment.points.append(point[0], point[1]) for point in data]

        # print('Created GPX:', gpx.to_xml())
        with open(file_name, "w") as f:
            f.write(gpx.to_xml())