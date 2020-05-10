from track_analyzer.repository.resource.gpx_resource import GPXResource
import utils
import gpxpy
import gpxpy.gpx
from track_analyzer.entities.track_point import TrackPoint as Point
from track_analyzer.conf.config import EXPORT_SIMULATIONS_GPX_FOLDER


def create_gpx_track(data):
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    [gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point[1], point[0])) for point in data]
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

    def write(self, uid, data):
        path = utils.create_folder(EXPORT_SIMULATIONS_GPX_FOLDER)
        with open(path + "/" + 'simulated_track_' + uid + '.gpx', 'w') as f:
            f.write(create_gpx_track(data))

