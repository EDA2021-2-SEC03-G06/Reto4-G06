"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from tabulate import simple_separated_format, tabulate
from DISClib.ADT.graph import gr, numEdges
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
assert cf

# ___________________________________________________
#  Variables
# ___________________________________________________


servicefile = 'bus_routes_50.csv'
initialStation = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
graphsfile,citiesfile,airportsfile = ("Skylines/routes-utf8-small.csv","Skylines/worldcities-utf8.csv","Skylines/airports-utf8-small.csv")

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar puntos de interconeccion aerea")
    print("3- Encontrar clusteres")
    print("4- Encontrar la ruta mas corta")
    print("5- Usar millas viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")
    print("7- Comparar con servicio web externo")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalogo = controller.init_catalogo()
        ultimo,primero = controller.load_data(graphsfile,citiesfile,airportsfile,catalogo)
        print("Numero de aeropuertos: ", gr.numVertices(catalogo["Vector"]))
        print("Numero de aeropuertos: ", gr.numVertices(catalogo["AntiVector"]))
        print("Numero de rutas: ", gr.numEdges(catalogo["Vector"]))
        print("Numero de rutas: ", gr.numEdges(catalogo["AntiVector"]))
        print("Total ciudades: ", m.size(catalogo["cities"]))
        ultimo = me.getValue(m.get(catalogo["cities"],ultimo))
        rta = [["Poblacion: ",ultimo["population"]],
                ["Latitud: ",ultimo["lat"]],
                ["Longitud: ",ultimo["lng"]]]
        print(tabulate(rta,tablefmt='grid'))
        primero = me.getValue(m.get(catalogo["airports"],primero))
        rta = [["Nombre: ",primero["Name"]],
                ["Latitud: ",primero["Latitude"]],
                ["Longitud: ",primero["Longitude"]],
                ["País: ", primero["Country"]],
                ["Ciudad: ", primero["City"]]]
        print(tabulate(rta,tablefmt='grid'))
    
    elif int(inputs[0]) == 2:
        vector, antivector, airports = controller.more_edges(catalogo)
        print("Hay ", airports," aeropuertos interconectados")
        lstkey = m.keySet(vector)
        for airport in lt.iterator(lstkey):
            current = m.get(catalogo["airports"],airport)
            current = me.getValue(current)
            print("-"*100)
            print("IATA: ",airport)
            print("Nombre: ",current["Name"])
            print("Ciudad: ", current["City"])
            print("Pais: ", current["Country"])
            print("Conexiones: ", me.getValue(m.get(vector,airport)))
            print("-"*100)
        lstkey = m.keySet(antivector)
        for airport in lt.iterator(lstkey):
            current = m.get(catalogo["airports"],airport)
            print(airport)
            if current != None:
                current = me.getValue(current)
                print("-"*100)
                print("IATA: ",airport)
                print("Nombre: ",current["Name"])
                print("Ciudad: ", current["City"])
                print("Pais: ", current["Country"])
                print("Conexiones: ", me.getValue(m.get(antivector,airport)))
                print("-"*100)
    elif int(inputs[0]) == 3:
        airport1 = input("¿Desde dónde desea iniciar (IATA)? ")
        airport2 = input("¿A dónde desea llegar (IATA)? ")
        scc_numero, igual = controller.SCC(catalogo,airport1,airport2)
        print("En el grafo hay ", scc_numero," componentes fuertemente conectados")
        print("Estos dos aeropuertos "+igual+" pertenecen al mismo cluster.")
    elif int(inputs[0]) == 4:
        begin = input("De que ciudad desea iniciar? ")
        begin_cities = controller.differenciation_city(begin,catalogo)
        for city in range(1,lt.size(begin_cities)+1):
            print(city, lt.getElement(begin_cities,city))
        begin = int(input("¿En que numero se encuentra la ciudad que le interesa?"))
        begin = lt.getElement(begin_cities,begin)
        end = input("De que ciudad desea llegar? ")
        end_cities = controller.differenciation_city(end,catalogo)
        for city in range(1,lt.size(end_cities)+1):
            print(city, lt.getElement(end_cities,city))
        end = int(input("¿En que numero se encuentra la ciudad que le interesa?"))
        end = lt.getElement(end_cities,end)
        controller.near_route(catalogo,begin,end)
    elif int(inputs[0]) == 5:
        pass
    elif int(inputs[0]) == 6:
        pass
    elif int(inputs[0]) == 7:
        pass
    else:
        sys.exit(0)
sys.exit(0)
