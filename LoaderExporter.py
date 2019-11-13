import abc

import gpxpy


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