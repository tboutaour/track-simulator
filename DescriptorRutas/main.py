from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import gpxpy
import numpy
import random


lat = []
lon = []

fig = plt.figure(facecolor = '0.05')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)
data_path = './gpx/prueba'
gpx_filename = './gpx/roads.gpx'

gpx_file = open(gpx_filename, 'r')
gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:
    colorin = numpy.random.rand(3,)
    print(track.name)
    for segment in track.segments:
        for point in segment.points:
            lat.append(point.latitude)
            lon.append(point.longitude)
    plt.plot(lon, lat, color= colorin, lw = 0.2, alpha = 0.8)
    lat = []
    lon = []

filename = data_path + '.png'
plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=300)