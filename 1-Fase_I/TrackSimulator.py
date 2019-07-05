# -*- coding: utf-8 -*-
"""
@author: tonibous
"""
import numpy as np
import pandas as pd

def GetRandomValue(data):
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    rnd = np.random.random()
    return np.argmax(np.array(ser_dx > rnd))

# def setFrequencyToNode(simulador,data):
#     #En item[0] tendremos (origen,destino)
#     #En item[1] tendremos porcentaje frecuencia
#
#     #la idea es ir al nodo, coger el atributo que corresponde con
#     #el destino y añadirle la frecuencia
#     for item in data:
#         simulador.Grafo.nodes[item[0][0]]['P_'+str(item[0][1])] = item[1]
#
#
# def getMostFrequentPathNode(node):
#     auxList = [(k, v) for k, v in simulador.Grafo.nodes[node].items() if 'P_' in k]
#     auxList = np.array(auxList)
#     frequentPoint = float(max(auxList,key=itemgetter(1))[0][2:])
#     return frequentPoint

