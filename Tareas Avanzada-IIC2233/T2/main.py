from dccampesino import Jardin
import sys 
import extras as ex
import parametros as prm
from dia import pasar_dia

nombres = []
for j in ex.lista_jardines:
    nombres.append(j[0])
diff = ["facil", "media", "dificil"]

iniciar = False
argumento = sys.argv
name = argumento[1].lower()
dificultad = argumento[2].lower()
if name not in nombres:
    print("Nombre de Jardin invalido")
    print(f"Nombres validos: {nombres}")
if dificultad not in diff:
    print("Dificultad invalida")
    print(f"Dificultades: {diff}")
if name in nombres and dificultad in diff:
    print("Iniciando DCCamplesino...")
    iniciar = True
    for j in ex.lista_jardines:
        if name == j[0]:
            tablero = j[1]
    jardin = Jardin(tablero) #JARDIN DE JUEGO
    dia = 0 #DIA INICIAL

#ACA EMPIEZA
seguir_j = False
seguir_l = False
if iniciar == True:
    while dia <= prm.DURACION:
        print(ex.menu_inicio)
        print(f"""Soles disponibles: {jardin.soles}\nTemperatura: {jardin.temperatura} °C
              \nDia actual: {dia}""")
        print(ex.menu_inicio_2)
        option = input("Indique su opcion:")
        if option in ["0", "1", "2", "3"]:
            option = int(option)
        else:
            print("Por favor, ponga un int válido")
        if option == 0: #SALIR
            print("Saliste de DCCampesino, supongo que vas a seguir tu camino...")
            print("Gracias por ayudar a Hernan a combatir los zombies!")
            print("Espero que no haya muerto... Bueno, hasta la proxima!")
            iniciar = False
            dia = (prm.DURACION +100) #Para asegurar
        elif option == 1: #MENU JARDIN
            seguir_j = True
            while seguir_j:
                print(ex.menu_jardin)
                for fila in jardin.tablero_plantas: 
                    print(f"{fila}")
                print(ex.menu_jardin_2)
                accion = input("Indique su opcion:")
                if accion in ["0", "1", "2", "3"]:
                    accion = int(accion)
                else:
                    print("Por favor, ponga un int válido")
                if accion == 0:
                    seguir_j = False
                elif accion == 1: #Intercambio
                    seguir = True
                    coords = ""
                    while seguir:
                        cy = input("Entregue fila que desea intercambiar: ")
                        if cy.isdigit():
                            cx = input("Entregue columna que desea intercambiar: ")
                            if cx.isdigit():
                                coords += f"{cy},{cx}"
                                seguir = False
                            else:
                                print("Entregue un numero por favor")
                        else:
                            print("Entregue un numero por favor")
                    seguir = True
                    while seguir: 
                        cy = input("Entregue otra fila que desea intercambiar: ")
                        if cy.isdigit():
                            cx = input("Entregue otra columna que desea intercambiar: ")
                            if cx.isdigit():
                                coords += f";{cy},{cx}"
                                seguir = False
                            else:
                                print("Entregue un numero por favor")
                        else:
                            print("Entregue un numero por favor")
                    cambio = jardin.intercambiar(coords)
                elif accion == 2: #Cultivar
                    inventario = jardin.inventario_plantas
                    if len(inventario) == 0:
                        print("No hay plantas para cultivar")
                    else:
                        print(f"Disponibles: {inventario}")
                        p = input("Selecciona la planta:")
                        try:
                            p = p.upper()
                        except:
                            print("Ingrese una letra por favor")
                        nombres = []
                        for planta in inventario:
                            if planta.tipo not in inventario:
                                nombres.append(planta.tipo)
                        if p not in nombres:
                            print("La planta no figura en el inventario")
                        elif p in nombres:
                            seguir = True
                            t = jardin.tablero
                            alto = len(t) - 1
                            ancho = len(t[0]) - 1
                            while seguir:
                                cy = input("Entregue fila donde desea cultivar: ")
                                if cy.isdigit():
                                    cy = int(cy)
                                    if cy >= 0 and cy <= alto:
                                        cx = input("Entregue columna donde desea cultivar: ")
                                        if cx.isdigit():
                                            cx = int(cx)
                                            if cx >= 0 and cx <= ancho:
                                                seguir = False
                                            else:
                                                print("Entregue un numero valido por favor")
                                        else:
                                            print("Entregue un numero valido por favor")
                                    else:
                                        print("Entregue un numero valido por favor")
                                else:
                                    print("Entregue un numero valido por favor")
                            jardin.cultivar_planta(p, cy, cx)
                elif accion == 3: #Regar
                    jardin.regar_plantas(dificultad)
        elif option == 2: #MENU LABORATORIO
            seguir_l = True
            while seguir_l:
                inventario = []
                for planta in jardin.inventario_plantas:
                    inventario.append(planta.tipo)
                print(ex.menu_lab)
                if len(inventario) == 0:
                    print(ex.menu_lab2_0)
                    print("No hay plantas para mutar")
                    seguir_l = False
                else:
                    tipos = ["S", "D", "P", "A", "C", "F"]
                    s, d = inventario.count("S"), inventario.count("D")
                    p, a = inventario.count("P"), inventario.count("A")
                    c, f = inventario.count("C"), inventario.count("F")
                    print(ex.menu_lab2(s, d, p, a, c, f))
                    accion = input("Indique su mutacion a crear:")
                    try:
                        accion = int(accion)
                    except:
                        print("Por favor escriba un int")
                    if accion == 0:
                        seguir_l = False
                    elif accion == 1: #Aresauce
                        jardin.mutar("A")
                    elif accion == 2:
                        jardin.mutar("C")
                    elif accion == 3:
                        jardin.mutar("F")
                    else:
                        print("Indique un int válido")
        elif option == 3:
            d = pasar_dia(jardin, dificultad)
            dia += d
            print("Te fuiste a dormir...zzz")
            print(f"Pasando a dia {dia}...")
            if dia == prm.DURACION:
                print("Ultimo dia nadie se enoja!")
            else:
                print("Buenos dias! A despertar!")
try:
    print(f"FIN DEL JUEGO\nPUNTUACION: {jardin.soles} soles\n")
    print("TU JARDIN:")
    print(jardin)
except:
    print("Revisa que todo esté bien!")