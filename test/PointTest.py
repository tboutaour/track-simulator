import unittest
from entities.TrackPoint_impl import TrackPoint as Point
from entities.TrackSegment_impl import TrackSegment as Segment

class MyTestCase(unittest.TestCase):
    def test_segment_operations(self):
        point = Point(2, 1)
        point_b = Point(4, 4)
        segm = Segment([point.get_latlong(), point_b.get_latlong()])

        self.assertEqual(point.get_longitude(), 1.0)
        self.assertEqual(point.haversine_distance(point_b), 400524.4343337236)
        self.assertEqual(segm.get_points(), [(2.0, 1.0), (4.0, 4.0)])
        self.assertEqual(segm.get_distance(), 400524.4343337236)
        segm.add_point(point.get_latlong())
        segm.add_point(point.get_latlong())
        self.assertEqual(segm.get_points(), [(2.0, 1.0), (4.0, 4.0), (2.0, 1.0), (2.0, 1.0)])
        self.assertEqual(point.get_bearing(point_b), 56.20251196993809)

    def test_point_operations(self):
        point = Point(2, 1)
        point_b = Point(4,4)
        self.assertEqual(point.get_latitude(), 2)
        self.assertEqual(point.get_longitude(), 1)
        self.assertEqual(point.haversine_distance(point_b), 400524.4343337236)


if __name__ == '__main__':
    unittest.main()

