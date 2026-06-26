from dccultivo import Predio, DCCultivo
import utils

menu_inicio =(
"""
¡Bienvenido a DCCultivo! \n
*** Menú de Inicio *** \n
[1] Crear predios \n
[2] Salir del programa \n
"""
)
menu_acciones =(
"""
¡Bienvenido a DCCultivo! \n
Tu terreno está listo para trabajar. \n
*** Menú de Acciones *** \n
[1] Visualizar predio \n
[2] Plantar \n
[3] Regar \n
[4] Buscar y eliminar plagas \n
[5] Salir del programa \n
"""
)
accion_ver =(
"""
DCCultivo: Visualizar predio \n
____________________________ \n
"""
)
accion_plantar =(
"""
DCCultivo: Plantar cultivos \n
____________________________ \n
"""
)
accion_regar =(
"""
DCCultivo: Regar cultivos \n
Recuerda tomar agua tambien! \n
____________________________ \n
"""
)
accion_plaga =(
"""
DCCultivo: Control de plagas \n
______________________________ \n
"""
)

def ver_predio() -> bool:
    print(accion_ver)
    codes_predios = []
    for predio in cultivo.predios:
        codes_predios.append(predio.codigo_predio)
    codes_predios.append("TODOS")
    print("Códigos de predios válidos:")
    for i in codes_predios:
        print(i)
    codigo = input("Indique el código del predio:")
    if codigo not in codes_predios:
        print("Código inválido")
        return True
    elif codigo in codes_predios:
        if codigo == "TODOS":
            for field in cultivo.predios:
                utils.imprimir_planos(field)
            return False
        for field in cultivo.predios:
            if codigo == field.codigo_predio:
                utils.imprimir_planos(field)
                return False

def plantar_cultivo() -> None:
    print(accion_plantar)
    codigo = input("Indique el código del cultivo para plantar:")
    codigo = int(codigo)
    alto = input("Indique el alto del bloque a plantar:")
    alto = int(alto)
    ancho = input("Indique el ancho del bloque a plantar:")
    ancho = int(ancho)
    result = cultivo.buscar_y_plantar(codigo, alto, ancho)
    if result == True:
        print(f"El resultado de la función es {result}.")
        print("Se logró encontrar un predio en el cual plantar.")
        print("Ahora visualiza los predios para ver los cambios!")
        return 
    elif result == False:
        print(f"El resultado de la función es {result}.")
        print("No se logró encontrar un predio en el cual plantar :(")
        return 

def regar_cultivo() -> None:
    print(accion_regar)
    codes_predios = []
    for predio in cultivo.predios:
        codes_predios.append(predio.codigo_predio)
    while True:
        print("Códigos de predios válidos:")
        for i in codes_predios:
            print(i)
        codigo = input("Indique el código del predio:")
        if codigo in codes_predios:
            break
        elif codigo not in codes_predios:
            print("Código inválido, seleccione nuevamente porfavor...")
    print("Indique las coordenadas del círculo a regar:")
    x = input("Fila:")
    x = int(x)
    y = input("Columna:")
    y = int(y)
    coords = [x, y]
    area = input("Indique el área a regar:")
    area = int(area)
    cultivo.buscar_y_regar(codigo, coords, area)
    print("Ahora revisa que tu predio haya sido regado.")
    return

def terminator_cultivo() -> None:
    print(accion_plaga)
    plagas = utils.plagas(cultivo)
    orden = cultivo.detectar_plagas(plagas)
    print("Plagas eliminadas con éxito.")
    print(orden)
    print("[Predio afectado, Celdas eliminadas]")
    return 
#
# ACÁ EMPIEZA
#
print(menu_inicio)

seguir = True
while seguir:
    opcion = input("Indique su opción (1 o 2):")
    opcion = int(opcion)
    if opcion == 2: # Salir
        print(f"Hasta la próxima!")
        seguir = False
    elif opcion == 1: # Acción
        seguir = False
    elif opcion not in [1, 2]: # Error
        print("Error! \n Tienes que escoger un int entre 1 o 2")

if opcion == 1:
    cultivo = DCCultivo()
    cultivo.crear_predios("predios.txt")
    seguir = True
while seguir:
    print(menu_acciones)
    opcion = input("Indique su opción (1, 2, 3, 4, 5):")
    opcion = int(opcion)

    if opcion == 5: # Salir
        print("Hasta la próxima!")
        seguir = False

    elif opcion == 1: # Visualizar
        ver = True
        while ver:
            ver = ver_predio()

    elif opcion == 2: # Plantar
        plantar_cultivo()

    elif opcion == 3: # Regar
        regar_cultivo()

    elif opcion == 4: # Plagas
        terminator_cultivo()
    
    elif opcion not in [1, 2, 3, 4, 5]: # Error
        print("Error! \n Tienes que escoger un int entre 1 y 5")
        