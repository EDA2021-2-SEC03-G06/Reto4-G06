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
 """

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# Inicialización del Catálogo de libros
def init_catalogo():
    return model.init_catalogo()

# Funciones para la carga de datos
def load_data(graphsfile,citiesfile,airportsfile,catalogo):
    graphsfile = cf.data_dir + graphsfile
    input_file = csv.DictReader(open(graphsfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        
        model.load_Graphs(service,catalogo)
    
    citiesfile = cf.data_dir + citiesfile
    input_file = csv.DictReader(open(citiesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        ultimo = service["city"]+"-"+service["country"]
        centinela = False
        model.loadcities(catalogo,service)

    airportsfile = cf.data_dir + airportsfile
    input_file = csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")
    
    centinela = True
    for service in input_file:
        if centinela:
            primero = service["IATA"]
            centinela = False
        model.load_airports(catalogo,service)
    return ultimo,primero

    
    
# Funciones de ordenamiento

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def differenciation_city(ciudad, catalogo):
    return model.differenciation_city(ciudad, catalogo)

def more_edges(catalogo):
    vector,airports = model.more_edges(catalogo["Vector"])
    antivector = model.more_edges(catalogo["AntiVector"])[0]
    return vector, antivector, airports

def SCC(catalogo, airport1,airport2):
    return model.clusters(catalogo,airport1,airport2)
def near_route(catalogo,ciudad1,ciudad2):
    return model.near_route(catalogo,ciudad1,ciudad2)