from src.track_analyzer.repository.resource.gpx_resource import GPXResource
import gpxpy
import gpxpy.gpx
from src.track_analyzer.entities.track_point import TrackPoint as Point


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


def load_file_points(file):
    points_a = []
    for track in file.tracks:  # OJO SOLO HAY UN TRACK
        for segment in track.segments:  # OJO SOLO HAY UN SEGMENT
            for iA in range(0, len(segment.points) - 1):
                point = segment.points[iA]
                points_a.append([point.longitude, point.latitude, Point(point.longitude, point.latitude)])
    return points_a


class GPXResourceImpl(GPXResource):

    def read(self, file_path):
        with open(file_path) as source_file:
            data = gpxpy.parse(source_file)
            points = load_file_points(data)
        return list(list(zip(*points))[2])

    def write(self, output, data):
        with open(output, "w") as f:
            f.write(data)

