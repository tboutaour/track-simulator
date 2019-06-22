# -*- coding: utf-8 -*-
"""
Created on Wed May  8 17:15:18 2019

@author: tonibous
"""
import gpxpy
import Grafo as g
import numpy as np
import osmnx as ox
import networkx as nx
from geopy.distance import distance, VincentyDistance
import matplotlib.pyplot as plt
import pandas as pd
import math
from geopy import Point
from operator import itemgetter


def GetDistPoint(point,routeGap):
#    nodes = data[(data[:, 2] == routeGap[0]) & (data[:, 3] == routeGap[1])][:, 0:2]
    nodes = df[(df['source'] == routeGap[0]) & (df['target'] == routeGap[1])]
    if nodes.size == 0:
        nodes = df[(df['source'] == routeGap[1]) & (df['target'] == routeGap[0])]
    try:
        coords = nodes.iloc[0].geometry.coords[:]
        coordList = [list(reversed(item)) for item in coords]
        return haversine_distance(point, coordList[closest_node(point, np.array(coordList))])
    except:
         return 0


def SimplifyRoute(simulador,data):
    exp = []
    exp.append(data[0])
    for idx in range(1,len(data)):
        distance = nx.shortest_path_length(simulador.Grafo,data[idx][2],data[idx-1][3])
        point = [data[idx][0],data[idx][1]]
        if distance == 0:
            exp.append(data[idx])
        elif 6 >= distance >= 1:
            routeGaps = (GetRoadGaps(data[idx][2],data[idx-1][3])).tolist()

            addedPoints = [[data[idx][0],data[idx][1]] + x + [GetDistPoint(point,x)] for x in routeGaps]
            exp.append(data[idx])
            exp.extend(addedPoints)

        else:
            print("distancia:" + str(distance))
    return np.array(exp)

def CargaPuntosTrack(fichero):
    points_a=[]
    for track in fichero.tracks:  # OJO SOLO HAY UN TRACK
        for segment in track.segments:  # OJO SOLO HAY UN SEGMENT
            for iA in range(0, len(segment.points) - 1):
                point = segment.points[iA]
                points_a.append([point.latitude, point.longitude])
    return np.array(points_a)

def ObtenerDistancia(puntos):
    distancia=[]
    for p in range(len(puntos)-1):
        distancia.append(distance(puntos[p],puntos[p+1]).m)
    return np.array(distancia)

def GetRouteFromPoint(grafo,data, points_a):
    originNode, destinyNode, distance = grafo.getClosestNodes(data,points_a)
    return np.column_stack((points_a,originNode,destinyNode,distance*1000))

def PlotPoints(ax, t, color):
    for a in t:
        lat = a[0]
        lon = a[1]
        ax.scatter(lon, lat, c= color, s=20)

def PlotRoute(simulador, track):
    routes = []
    for i in track:
        routes.append(nx.shortest_path(simulador.Grafo, i[2], i[3], weight='length'))

    ox.plot_graph_routes(simulador.Grafo, routes, route_linewidth=1, orig_dest_node_size=3)
        
#Función para generar el array bidimensional con todos los puntos y sus nodos or. fin.
def TreeStructureCreation(df):
    roadRelation = df[['source','target','geometry']]
    n = []
    for road in roadRelation.iterrows():
        try:
            coords = road[1].geometry.coords[:]
            coordList = [list(reversed(item)) for item in coords]
            L = [ x + [road[1].source,road[1].target] for x in coordList]
            n.extend(L)
        except AttributeError:
            pass
    return np.array(n)

#...................................................................    
#Método que muestra el cálculo de la distancia. Muestra histograma
#...................................................................
def CalculoDistanciaTrayectorias(n):
    rout ="Rutas/Ficheros/RutaCastilloBellver"
    d=[]
    for i in range(n):
        rout ="Rutas/Ficheros/RutaCastilloBellver"
        rout=rout+str(i+1)+".gpx"
        f1 = open(rout)
        p1 = gpxpy.parse(f1)
        points_a=[]
        for track in p1.tracks:  # OJO SOLO HAY UN TRACK
            for segment in track.segments:  # OJO SOLO HAY UN SEGMENT
                for iA in range(0, len(segment.points) - 1):
                    point = segment.points[iA]
                    points_a.append((point.latitude, point.longitude))
        for p in range(len(points_a)-1):
            d.append(distance(points_a[p],points_a[p+1]).m)
        
    plt.hist(d, bins=70)
    
    plt.xlabel('distance')
    plt.show()

def GetRoadGaps(origin,target):
    route = nx.shortest_path(simulador.Grafo,origin,target)
    points = []
    for i in range(0,len(route)-1):
        points.append((route[i],route[i+1]))
    return np.array(points)

def GetFrequency(data,title):
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    fig, ax = plt.subplots()
    ax = ser_dx.plot(drawstyle='steps', legend="True")
    ax.set_xlabel(title, fontsize=16)
    ax.set_ylabel("Frequency", fontsize=16)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    ax.legend().set_visible(False)
    ax.grid(True)
    fig.canvas.draw()

def closest_node(node, nodes):
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)

def haversine_distance(origin, destination):
  """ Haversine formula to calculate the distance between two lat/long points on a sphere """
  radius = 6371.0 # FAA approved globe radius in km
  dlat = math.radians(destination[0]-origin[0])
  dlon = math.radians(destination[1]-origin[1])
  a = math.sin(dlat/2.) * math.sin(dlat/2.) + math.cos(math.radians(origin[0])) \
      * math.cos(math.radians(destination[0])) * math.sin(dlon/2.) * math.sin(dlon/2.)
  c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = radius * c

  return d*1000

def calculate_initial_compass_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")
    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])
    diffLong = math.radians(pointB[1] - pointA[1])
    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
    * math.cos(lat2) * math.cos(diffLong))
    initial_bearing = math.atan2(x, y)
    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing

def GetDiagrams(data,title,bins):
    GetHistogram(data,title,bins)
    plt.show()
    GetFrequency(data, title)
    plt.show()

def GetHistogram(data,title,bins):
    fig, ax = plt.subplots()
    plt.hist(data, bins=bins)
    ax.set_xlabel(title, fontsize=16)
    ax.set_ylabel("Frequency", fontsize=16)
    ax.grid(True)
    fig.canvas.draw()

def GetBearingPointToPoint(set):
    angulos = []
    for idx in range(0, len(set) - 1):
        point = tuple(set[idx])
        nextPoint = tuple(set[idx + 1])
        deg = calculate_initial_compass_bearing(point, nextPoint)
        angulos.append(deg)

    angSinCero = [x for x in angulos if x != 0]
    return  angSinCero

def GetDistancePointToPoint(set):
    DistanceBetweenPonints = []
    for idx in range(0,len(set)-1):
        distan = haversine_distance(set[idx],
                                    set[idx+1])
        DistanceBetweenPonints.append(distan)
    DistanceBetweenPonints = [x for x in DistanceBetweenPonints if x != 0]
    return DistanceBetweenPonints

def GetRandomValue(data):
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    rnd = np.random.random()
    return np.argmax(np.array(ser_dx > rnd))


#...................................................................    
#Primer Main.
#Genera a partir de un fichero todo el grafo y una comparación con una ruta
#...................................................................

route1 = "Rutas/Ficheros/RutaRealCastell1.gpx"
f1 = open(route1)
p1 = gpxpy.parse(f1)

points_c=[]

puntos_track = CargaPuntosTrack(p1)

distancia = ObtenerDistancia(puntos_track)

simulador = g.Grafo(39.5713,39.5573,2.6257,2.6023,p1)
simulador.Grafo = simulador.Grafo.to_undirected()

df=nx.to_pandas_edgelist(simulador.Grafo)
data = TreeStructureCreation(df)
simulador.GenerarKDtreeSegmentos(data)

trackRouteRelation = GetRouteFromPoint(simulador,data,puntos_track)

trackRouteRelationFiltered = SimplifyRoute(simulador,trackRouteRelation)

fig, ax = ox.plot_graph(simulador.Grafo, fig_height=10, fig_width=10, 
            show=False, close=False, 
            edge_color='black')

PlotPoints(ax, puntos_track, 'red')
# originNodes = simulador.GetNodePoints(trackRouteRelation[:,2])
# destinNodes = simulador.GetNodePoints(trackRouteRelation[:,3])
# PlotPoints(ax, originNodes, 'green')
# PlotPoints(ax,destinNodes, 'green')
PlotPoints(ax, trackRouteRelationFiltered[:,0:2], 'blue')

originNodes = simulador.GetNodePoints(trackRouteRelationFiltered[:,2])
destinNodes = simulador.GetNodePoints(trackRouteRelationFiltered[:,3])
PlotPoints(ax, originNodes, 'orange')
PlotPoints(ax,destinNodes, 'orange')

PlotRoute(simulador,trackRouteRelationFiltered)

GetFrequency(trackRouteRelationFiltered[:,4],"Distance Point-Route Meters")

plt.show(block=True)

bearing = GetBearingPointToPoint(trackRouteRelationFiltered[:,0:2])
distancePointPoint = GetDistancePointToPoint(trackRouteRelationFiltered[:,0:2])

GetDiagrams(bearing,"Bearing,meters",100)
GetDiagrams(distancePointPoint,"Distance Point-Point,meters",100)



def simularPuntos(PuntoInicial):
    PuntoOrigen = PuntoInicial
    for i in range(0,10):
        distanceRandomPointPoint = GetRandomValue(distancePointPoint)
        bearingRandomValue = GetRandomValue(bearing)
        point = VincentyDistance(meters=distanceRandomPointPoint).destination(Point(PuntoOrigen[0],PuntoOrigen[1]), bearingRandomValue)
        PlotPoints(ax,[np.array([point[0],point[1]])],'black')
        PuntoOrigen = point
#distance(kilometers=distanceRandomPointPoint).destination(Point(39.5585311,2.6140847), bearingRandomValue)


# fig, ax = ox.plot_graph(simulador.Grafo, fig_height=10, fig_width=10,
#             show=False, close=False,
#             edge_color='black')
# simularPuntos(Point(trackRouteRelationFiltered[40][0], trackRouteRelationFiltered[40][1]))
# plt.show()


# for node in simulador.Grafo.nodes:
#     relatedEdges = np.array([e for e in simulador.Grafo.edges(node)])
#     for edge in relatedEdges[:,1]:
#         valor = {node: 0.0}
#         name = str(edge)
#         nx.set_node_attributes(simulador.Grafo, values=valor, name= name)



def getFrequencyRoute(data):
    cabecera = np.array(['X','Y','Origen','Destino','Exactitud'])
    dftemps = pd.DataFrame({'Origen':data[:,2],'Destino':data[:,3]})
    frequency = dftemps.groupby(["Origen", "Destino"]).size()
    pFrequency = frequency/ frequency.sum()
    return np.array([[b, c] for b, c in pFrequency.items()])


def setFrequencyToNode(simulador,data):
    #En item[0] tendremos (origen,destino)
    #En item[1] tendremos porcentaje frecuencia

    #la idea es ir al nodo, coger el atributo que corresponde con
    #el destino y añadirle la frecuencia
    for item in data:
        simulador.Grafo.nodes[item[0][0]]['P_'+str(item[0][1])] = item[1]


def getMostFrequentPathNode(node):
    auxList = [(k, v) for k, v in simulador.Grafo.nodes[node].items() if 'P_' in k]
    auxList = np.array(auxList)
    frequentPoint = float(max(auxList,key=itemgetter(1))[0][2:])
    return frequentPoint
