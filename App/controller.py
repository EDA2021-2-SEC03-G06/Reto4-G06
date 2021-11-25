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
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
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

# Funciones de consulta sobre el catálogo
