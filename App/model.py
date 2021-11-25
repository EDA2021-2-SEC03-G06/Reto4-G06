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
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
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
        return catalogo
    except Exception as exp:
        error.reraise(exp, 'model:init_catalog')

# Funciones para agregar informacion al catalogo
def addStop(graph, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(graph, stopid):
            gr.insertVertex(graph, stopid)
        return graph
    except Exception as exp:
        error.reraise(exp, 'model:addStop')

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
    return catalogo

def load_airports(catalogo,aeropuerto):
    m.put(catalogo["airports"],aeropuerto["IATA"],aeropuerto)
    city = aeropuerto['City'] + "-" + aeropuerto["Country"]
    entry = m.get(catalogo["cities"],city)
    if entry != None:
        info = me.getValue(entry)
        lt.addLast(info["aeropuertos"],aeropuerto["IATA"])

# Funciones para creacion de datos

# Funciones de consulta

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

# Funciones de ordenamiento
