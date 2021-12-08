"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config
from haversine import haversine as hv
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import graphstructure as gp
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# Construccion de modelos
def init_catalogo():
    try:
        catalogo = {}
        catalogo["Vector"] = gr.newGraph(datastructure='ADJ_LIST',
                                                directed=True,
                                                size=14000,
                                                comparefunction= None)
        catalogo["AntiVector"] = gr.newGraph(datastructure='ADJ_LIST',
                                                directed=False,
                                                size=14000,
                                                comparefunction= None)
        catalogo["airports"] = m.newMap()
        catalogo["cities"] = m.newMap()
        catalogo["namesakes"] = m.newMap()
        return catalogo
    except Exception as exp:
        error.reraise(exp, 'model:init_catalog')

# Funciones para agregar informacion al catalogo
def addStop(graph, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(graph, stopid):
        gr.insertVertex(graph, stopid)
    return graph

def addConnection(graph, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(graph, origin, destination)
    if edge is None:
        gr.addEdge(graph, origin, destination, distance)
    return graph

def load_Graphs(service,catalogo):
    departure = service["Departure"]
    destiny = service["Destination"]
    distance = float(service["distance_km"])
    addStop(catalogo["Vector"],departure)
    addStop(catalogo["Vector"],destiny)
    addConnection(catalogo["Vector"],departure,destiny,distance)
    if gr.getEdge(catalogo["Vector"],destiny,departure) != None:
        addStop(catalogo["AntiVector"],departure)
        addStop(catalogo["AntiVector"],destiny)
        addConnection(catalogo["AntiVector"],departure,destiny,distance)
    return catalogo

def loadcities(catalogo,ciudad):
    city = ciudad["city"] + "-" + ciudad["country"]
    ciudad["aeropuertos"] = lt.newList(datastructure="ARRAY_LIST")
    m.put(catalogo["cities"],city,ciudad)
    map = catalogo["namesakes"]
    entry = m.get(map,ciudad["city"])
    if entry is None:
        datentry = lt.newList()
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry, city)
    m.put(catalogo["namesakes"], ciudad["city"], datentry)
    
    return catalogo

def load_airports(catalogo,aeropuerto):
    m.put(catalogo["airports"],aeropuerto["IATA"],aeropuerto)
    city = aeropuerto['City'] + "-" + aeropuerto["Country"]
    entry = m.get(catalogo["cities"],city)
    if entry != None:
        info = me.getValue(entry)
        lt.addLast(info["aeropuertos"],aeropuerto["IATA"])




# ==============================
# Funciones de consulta
# ==============================
def differenciation_city(ciudad, catalogo):
    cities = m.get(catalogo["namesakes"],ciudad)
    if cities != None:
        cities = me.getValue(cities)
    return cities

def more_edges(grafo):
    lstvert = gp.vertices(grafo)
    airports = lt.size(lstvert)
    top_5 = m.newMap()
    n = 0
    while n < 5:
        maxvert = None
        maxdeg = 0
        for vert in lt.iterator(lstvert):
            degree = gp.outdegree(grafo,vert) * gp.indegree(grafo,vert)
            if(degree > maxdeg) and not m.contains(top_5,vert):
                maxvert = vert
                maxdeg = degree
        m.put(top_5,maxvert,maxdeg)
        n+=1
    return top_5, airports

def clusters(catalogo,airport1,airport2):
    SCC = scc.KosarajuSCC(catalogo["Vector"])
    print(SCC)
    numero_SCC = SCC["components"]
    Existe = "NO"
    if m.contains(SCC["idscc"],airport1) and m.contains(SCC["idscc"],airport2):
        airport_1 = me.getValue(m.get(SCC["idscc"],airport1))
        airport_2 = me.getValue(m.get(SCC["idscc"],airport2))
        if airport_1 == airport_2:
            Existe = "SI"
    return numero_SCC, Existe

def near_route(catalogo,ciudad1,ciudad2):
    ciudad_1 = me.getValue(m.get(catalogo["cities"],ciudad1))
    ciudad_2 = me.getValue(m.get(catalogo["cities"],ciudad2))
    if lt.size(ciudad_1["aeropuertos"]) != 0:
        aeropuerto_min_ciudad1 = None
        distancia_min_ciudad1 = 1*10**100
        for aeropuerto in lt.iterator(ciudad_1["aeropuertos"]):
            airport = me.getValue(m.get(catalogo["airports"],aeropuerto))
            ciudad = (float(me.getValue(m.get(catalogo["cities"],ciudad1))["lat"]),float(me.getValue(m.get(catalogo["cities"],ciudad1))["lng"]))
            airport_lt = (float(airport["Latitude"]),float(airport["Longitude"]))
            distancia = hv(ciudad,airport_lt)
            if distancia < distancia_min_ciudad1:
                distancia_min_ciudad1 = distancia
                aeropuerto_min_ciudad1 = aeropuerto
    else:
        print("Pa que quieres hacer eso?1")
        aeropuerto_min_ciudad1 = None
        distancia_min_ciudad1 = 1*10**100
        for aeropuerto in lt.iterator(m.keySet(catalogo["airports"])):
            airport = me.getValue(m.get(catalogo["airports"],aeropuerto))
            ciudad = (float(me.getValue(m.get(catalogo["cities"],ciudad1))["lat"]),float(me.getValue(m.get(catalogo["cities"],ciudad1))["lng"]))
            airport_lt = (float(airport["Latitude"]),float(airport["Longitude"]))
            distancia = hv(ciudad,airport_lt)
            if distancia < distancia_min_ciudad1:
                distancia_min_ciudad1 = distancia
                aeropuerto_min_ciudad1 = aeropuerto
    if  lt.size(ciudad_2["aeropuertos"]) != 0:
        aeropuerto_min_ciudad2 = None
        distancia_min_ciudad2 = 1*10*100
        for aeropuerto in lt.iterator(ciudad_2["aeropuertos"]):
            airport = me.getValue(m.get(catalogo["airports"],aeropuerto))
            ciudad = (float(me.getValue(m.get(catalogo["cities"],ciudad2))["lat"]),float(me.getValue(m.get(catalogo["cities"],ciudad2))["lng"]))
            airport_lt = (float(airport["Latitude"]),float(airport["Longitude"]))
            distancia = hv(ciudad,airport_lt)
            if distancia < distancia_min_ciudad2:
                distancia_min_ciudad2 = distancia
                aeropuerto_min_ciudad2 = aeropuerto
    else:
        print("Pa que quieres hacer eso?2")
        aeropuerto_min_ciudad2 = None
        distancia_min_ciudad2 = 1*10**100
        for aeropuerto in lt.iterator(m.keySet(catalogo["airports"])):
            airport = me.getValue(m.get(catalogo["airports"],aeropuerto))
            ciudad = (float(me.getValue(m.get(catalogo["cities"],ciudad2))["lat"]),float(me.getValue(m.get(catalogo["cities"],ciudad2))["lng"]))
            airport_lt = (float(airport["Latitude"]),float(airport["Longitude"]))
            distancia = hv(ciudad,airport_lt)
            if distancia < distancia_min_ciudad2:
                distancia_min_ciudad2 = distancia
                aeropuerto_min_ciudad2 = aeropuerto
    rutas = djk.Dijkstra(catalogo["Vector"],aeropuerto_min_ciudad1)
    camino_min = djk.pathTo(rutas,aeropuerto_min_ciudad2)
    

    return camino_min,(distancia_min_ciudad1+distancia_min_ciudad2)

# ==============================
# Funciones Helper
# ==============================

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name


# ==============================
# Funciones de Comparacion
# ==============================


def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

# Funciones utilizadas para comparar elementos dentro de una lista
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1