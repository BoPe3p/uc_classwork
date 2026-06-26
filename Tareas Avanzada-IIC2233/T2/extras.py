import os

def get_ruta(nombre_archivo: str) -> list:
    ruta = os.path.join("data", nombre_archivo)
    comprobar = os.path.exists(ruta)
    if comprobar == True:
        if nombre_archivo == "jardines.txt":
            with open(ruta, "rt", encoding= "utf-8") as archivo:
                lineas = archivo.readlines()
            for i in range(len(lineas)):
               lineas[i] = lineas[i].strip().split('!')
            jardines = []
            for linea in lineas:
                lista = []
                nombre = linea[0]
                contenido = linea[1]
                tablero = []
                filas = contenido.split(';')
                for elemento in filas:
                    e = elemento.split(',')
                    tablero.append(e)
                lista = [nombre, tablero]
                jardines.append(lista)
            return jardines
        
        elif nombre_archivo == "plantas.txt":
            with open(ruta, "rt") as archivo:
                lineas = archivo.readlines()
            for i in range(len(lineas)):
               lineas[i] = lineas[i].strip().split(';')
            lista = []
            for planta in lineas:
                contador = 0
                tipo = planta[0]
                if len(tipo) == 1:
                    contador += 1
                vida_max = int(planta[1])
                if vida_max <= 100 and vida_max >= 0:
                    contador += 1
                vida = int(planta[2])
                if vida <= vida_max and vida >= 0:
                    contador += 1
                res = int(planta[3])
                if res <= 40 and res >= 0:
                    contador += 1
                res_termica = int(planta[4])
                if res_termica <= 25 and res_termica >= -5:
                    contador += 1
                try:
                    congelacion = int(planta[5])
                    congelacion = bool(congelacion)
                except:
                    print("congelacion tiene que ser un str 0 o 1")
                altura = int(planta[6])
                if altura <= 30 and altura >= 0:
                    contador += 1
                if contador == 6:
                    plant = [tipo, vida_max, vida, res, res_termica, congelacion, altura]
                    lista.append(plant)
            return lista
        
        elif nombre_archivo == "eventos.txt":
            with open(ruta, "rt") as archivo:
                lineas = archivo.readlines()
            for i in range(len(lineas)):
               lineas[i] = lineas[i].strip().split(';')
            events = []
            for evento in lineas:
                lista = [] 
                nombre = evento[0]
                facil = float(evento[1])
                media = float(evento[2])
                dificil = float(evento[3])
                lista = [nombre, facil, media, dificil]
                events.append(lista)
            return events
    
lista_eventos = get_ruta("eventos.txt")
lista_jardines = get_ruta("jardines.txt")
lista_plantas = get_ruta("plantas.txt")
stats_plantas = {lista[0]: lista[1:] for lista in lista_plantas}

#Acciones
print_espacio=("=======================================\n")
print_regar = ("""
=========================\n
Se han regado tus plantas\n         
=========================               
""")
print_soles = ("""
=======================================\n
Se ha iniciado la produccion de soles\n         
=======================================               
""")
#Menus:
menu_inicio =(
f"""
--------------------- \n
---> DCCampesino <--- \n
--------------------- \n
*** Menú de Inicio *** \n
--------------------- \n
"""
)
menu_inicio_2 =("""
\n
[1] Menu jardin \n
[2] Laboratorio \n
[3] Pasar dia \n
[0] Salir del programa \n
""")
menu_jardin = ("""
--------------------- \n
    *** Jardin *** \n
--------------------- \n
""")
menu_jardin_2 = (f""" 
\n
[1] Intercambiar \n
[2] Cultivar \n
[3] Regar (Cuesta 10 soles)\n
\n
[0] Volver a Menu de Inicio \n
""")
menu_lab = (""" 
====================== \n
 *** Laboratorio *** \n
====================== \n
        |Guia|
----------------------------------------------
[1] Solaretillo + Defensauce    = Aresauce
[2] Solaretillo + Potencilantro = Cilantrillo
[3] Defensauce + Potencilantro  = Fensaulantro
----------------------------------------------""")
menu_lab2_0 = (f""" 
            |Tienes|
Solaretillo: {0} Defensauce: {0}  Potencilantro: {0}
----------------------------------------------------------
            |Mutaciones|
----------------------------------------------------------
Aresauce: {0}  Cilantrillo: {0}  Potencilantro: {0}
\n[0] Volver al Menu principal
""")
def menu_lab2(s: int, d: int, p: int, a: int, c: int, f: int) -> str:
    menu_lab2 = (f""" 
            |Tienes|
Solaretillo: {s} Defensauce: {d}  Potencilantro: {p}
----------------------------------------------------------
            |Mutaciones|
----------------------------------------------------------
Aresauce: {a}  Cilantrillo: {c}  Fensaulantro: {f}
\n[0] Volver al Menu principal
""")
    return menu_lab2
    
#Eventos
tranquilo = (f"""
==================================
        Es un dia tranquilo
==================================             
""")
helada = (f"""
====================================================================\n
                  Se ha activado el evento: Helada\n
====================================================================\n
   Las plantas con baja temperatura verán reducida su produccion\n      
====================================================================\n
""")
oleada = (f"""
====================================================================\n
            Se ha activado el evento: Oleada de Zombies\n
====================================================================\n
        Espero que tu jardin esté listo, porque pegan muy duro!\n      
====================================================================\n
""")