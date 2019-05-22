#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 19:05:45 2019

@author: tonibous
"""


#from os import listdir
#from os.path import isfile, join
import matplotlib.pyplot as plt
import gpxpy
import numpy
#import random
import time

cango = True
lat = []
lon = []

fig = plt.figure(facecolor = '0.05')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)
data_path = 'Rutas'
gpx_filename = 'CastilloBellver.gpx'
numero = 1
nombreFichero = "RutaCastilloBellver"

gpx_file = open(gpx_filename, 'r')
gpx = gpxpy.parse(gpx_file)

track = gpx.tracks[0]

gpx_aux = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()

for track in gpx.tracks:
    colorin = numpy.random.rand(3,)
    for segment in track.segments:
        print(nombreFichero+str(numero)+".gpx")
        f = open(data_path+"/Ficheros/"+nombreFichero+str(numero)+".gpx", "a")
        gpx_track.segments.append(segment)
        for point in segment.points:
            lat.append(point.latitude)
            lon.append(point.longitude)
        plt.plot(lon, lat, color= colorin, lw = 0.3, alpha = 0.8)
        lat.clear()
        lon.clear()
        gpx_aux.tracks.append(gpx_track)
        f.write(gpx_aux.to_xml())
        f.close()
        gpx_aux.tracks.clear()
        filename = data_path+"/Imagenes/" +time.strftime("%H:%M:%S")  +'.png'
        print (filename)
        plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=3, dpi=300)
        plt.clf()
        gpx_track.segments.clear()
        numero += 1
    
#Creación del fichero


#Inpresión del mapa

#filename = data_path +time.strftime("%H:%M:%S")  +'.png'
#print (time.strftime("%H:%M:%S"))
#plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=3, dpi=300)
#plt.show()

