#from os import listdir
#from os.path import isfile, join
import matplotlib.pyplot as plt
import gpxpy
import numpy
#import random
#import time

cango = True
lat = []
lon = []

fig = plt.figure(facecolor = '0.05')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)
data_path = './gpx/prueba'
gpx_filename = './gpx/roads.gpx'



l_osm_id = ['242957861.0','488473721,0','242957864.0','242957863.0','55702248.0','488473706.0','488473704.0','146217493.0','242957862.0','242957859.0','242957865.0','146217486.0','117628041.0','146217488.0','117627664.0','121211506.0','80624518.0','146217490.0','488473700.0','488473695.0','117630495.0','488473694.0','121208897.0','121814904.0','488473717.0','488473698.0','126532331.0','117626680.0','55697921.0','44060132.0','488473725.0','488473727.0','119432568.0','121228360.0','121228359.0','488473697.0','488473699.0','121228357.0','121228358.0','117629091.0','272670822.0','482305789.0','272670821.0','55170709.0','55170708.0','216998776.0','108908053.0','218521617.0','117629794.0','488473696.0','272670824.0','272670825.0','272670823.0','55262541.0','55170718.0','55170715.0','55170714.0','218519358.0','418119125.0','218519357.0','55170710.0','55170705.0','55170720.0','28913366.0','216999071.0','55695596.0','110514361.0','146217491.0','110514360.0','28913499.0','108910149.0','108911462.0','216998780.0','108909677.0','216998778.0','44060131.0','110514355.0','110514359.0','108929528.0','117628948.0','117626258.0','110514353.0','110514354.0','117626161.0','117629857.0','121208751.0','121211660.0','119432322.0','146217492.0','123213691.0','28913708.0','121814905.0','146216659.0','620486025.0','371314056.0','121208692.0','371314085.0','108910151.0','216998775.0','28913707.0','121208691.0']

gpx_file = open(gpx_filename, 'r')
gpx = gpxpy.parse(gpx_file)

track = gpx.tracks[1]

gpx_aux = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()

for track in gpx.tracks:
    colorin = numpy.random.rand(3,)
    
    for n in track.extensions:
        if (n.tag == "{http://osgeo.org/gdal}osm_id"):
            print("oms_uid")
            print(n.text)
            if n.text in l_osm_id:
                print("Ruta eliminada")
                cango = True
                break
        else:
            cango = False
            
            
    if(cango == True):
        for segment in track.segments:
            gpx_track.segments.append(segment)
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
        plt.plot(lon, lat, color= colorin, lw = 0.3, alpha = 0.8)
        lat = []
        lon = []
gpx_aux.tracks.append(gpx_track)
print(gpx_aux.to_xml())

#Creación del fichero
f = open("ejemplo.gpx", "a")
f.write(gpx_aux.to_xml())
f.close()

#Inpresión del mapa

#filename = data_path +time.strftime("%H:%M:%S")  +'.png'
#print (time.strftime("%H:%M:%S"))
#plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=3, dpi=300)
#plt.show()

