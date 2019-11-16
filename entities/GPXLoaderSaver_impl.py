from entities.LoaderSaver import LoaderSaver
import gpxpy
import gpxpy.gpx


def create_gpx_track(data):
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
    return gpx.to_xml()


class GPXLoaderSaver(LoaderSaver):

    def __init__(self, source):
        self.source = source
        self.source_file = self.loadFile()

    def loadFile(self):
        return open(self.source)

    def parseFile(self):
        data = gpxpy.parse(self.source_file)
        return data

    def saveFile(self, output, data):
        with open(output, "w") as f:
            f.write(data)

