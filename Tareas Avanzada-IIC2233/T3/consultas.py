from typing import Any, Generator, Iterable
from functools import reduce
from itertools import tee, islice, chain, cycle
from collections import defaultdict, Counter
from utilidades import Pizzas, Locales, Pedidos, ContenidoPedidos

# Carga de datos

def cargar_pizzas(path: str) -> Generator:
    with open(path, "r", encoding = "UTF-8") as info_pizzas:
        next(info_pizzas)
        for line in info_pizzas:
            pizza = line.strip().split(",")
            picsa = Pizzas(pizza[0], pizza[1], int(pizza[2]))
            yield picsa

def cargar_locales(path: str) -> Generator:
    with open(path, "r", encoding = "UTF-8") as info_locales:
        next(info_locales)
        for line in info_locales:
            local = line.strip().split(",")
            l = Locales(int(local[0]), local[1], local[2], local[3], int(local[4]))
            yield l

def cargar_pedidos(path: str) -> Generator:
    with open(path, "r", encoding = "UTF-8") as info_pedidos:
        next(info_pedidos)
        for line in info_pedidos:
            pedido = line.strip().split(",")
            p = Pedidos(int(pedido[0]), int(pedido[1]), int(pedido[2]), pedido[3], pedido[4])
            yield p

def cargar_contenido_pedidos(path: str) -> Generator:
    with open(path, "r", encoding = "UTF-8") as info_contenido:
        next(info_contenido)
        for line in info_contenido:
            content = line.strip().split(",")
            c = ContenidoPedidos(int(content[0]), content[1], int(content[2]), float(content[3]))
            yield c

# Consultas que ocupan 1 generador

def pedidos_con_al_menos_esta_pizza(
        generador_contenido_pedidos: Generator,
        tipo_de_pizza: str
        ) -> Iterable:
    for pedido in generador_contenido_pedidos:
        nombre = pedido.nombre.split("_")
        if tipo_de_pizza == nombre[0]:
            yield pedido

def cantidad_vendida_de_pizza_por_tipo(
        generador_contenido_pedidos: Generator,
        tipo_de_pizza: str
        ) -> int:
    gen_pizzas = filter(lambda pedido: pedido.nombre.split("_")[0] == tipo_de_pizza,
                         generador_contenido_pedidos)
    cantidad = reduce(lambda vendidas, x: vendidas + x.cantidad, gen_pizzas, 0)
    return cantidad

def pedido_con_mayor_descuento_utilizado(
        generador_contenido_pedidos: Generator
        ) -> Iterable:
    g1, g2 = tee(generador_contenido_pedidos, 2)
    mayor = max(pedido.descuento for pedido in g1)
    return filter(lambda pedido: pedido.descuento == mayor, g2)

def ajustar_precio_segun_ingredientes(
        generador_pizzas: Generator,
        ingrediente: str,
        diferencia_precio: int
        ) -> Iterable:
    pizzas = filter(lambda picsa: ingrediente in picsa.ingredientes.split(";"), generador_pizzas)
    for pizza in pizzas:
        presio = pizza.precio
        presio += diferencia_precio
        if presio < 7000:
            presio = 7000
        yield Pizzas(pizza[0], pizza[1], presio)

def clientes_despues_hora(
        generador_pedidos: Generator,
        hora: str
        ) -> str:
    hr = int(hora.split(":")[0])
    min = int(hora.split(":")[1])
    clientes = map(lambda c: str(c.id_cliente), 
                   filter(lambda p: (int(p.hora.split(":")[0]) > hr) or 
                          int(p.hora.split(":")[0]) == hr and (int(p.hora.split(":")[1]) >= min)
                      , generador_pedidos))
    a = " ".join(clientes)
    return a

def cliente_indeciso(
        generador_pizzas: Generator,
        ingrediente_no_deseado: str,
        cantidad_pizzas: int
        ) -> Iterable:
    pizzas = filter(lambda p: ingrediente_no_deseado.lower() not in
                     p.ingredientes.lower().split(";"), generador_pizzas)
    pizzas1, pizzas2 = tee(pizzas, 2)
    x = list(islice(pizzas1, cantidad_pizzas))
    n = len(x)
    if n < cantidad_pizzas:
        repetidas = islice(cycle(x), cantidad_pizzas - n)
        return chain(pizzas2, repetidas)
    else:
        return islice(pizzas2, cantidad_pizzas)

def pizzas_con_ingrediente(
        generador_pizzas: Generator,
        ingrediente: str
        ) -> Iterable:
    return filter(lambda pizza: ingrediente in pizza.ingredientes.split(";"), generador_pizzas)

def pizzas_pagables_de_un_tamano(
        generador_pizzas: Generator,
        dinero: int,
        tamano: str
    ) -> Iterable:
    pizzas = filter(lambda pizza: pizza.nombre.split("_")[1] == tamano.upper(), generador_pizzas)
    return filter(lambda pizza: pizza.precio <= dinero, pizzas)

def cantidad_empleados_pais(
        generador_locales: Generator,
        pais: str
        ) -> int:
    locales = filter(lambda local: local.pais == pais, generador_locales)
    return reduce(lambda empleados, i: empleados + i.cantidad_trabajadores, locales, 0)

# Consultas que ocupan 2 Generadores

def ganancias_producidas_en_los_pedidos(
        generador_contenido_pedidos: Generator,
        generador_pizzas: Generator
        ) -> Iterable:
    pizzas_precio = map(lambda p: (p.nombre, p.precio), generador_pizzas)
    dic = defaultdict()
    for p in pizzas_precio:
        dic[p[0]] = p[1]
    ganancias = defaultdict(int)
    for pedido in generador_contenido_pedidos:
        if pedido.nombre in dic.keys():
            ganancia = dic[pedido.nombre]
            ganancia *= pedido.cantidad
            dscto = float(1) - float(pedido.descuento)
            ganancia *= dscto
            ganancia = round(ganancia)
            if pedido.id_pedido not in ganancias.keys():
                ganancias[pedido.id_pedido] = ganancia
            else:
                ganancias[pedido.id_pedido] += ganancia
    for id in ganancias.keys():
        yield (id, ganancias[id])

def pizza_mas_vendida_del_dia(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        fecha: str
        ) -> set:
    dia = filter(lambda pedido: fecha == pedido.fecha, generador_pedidos)
    ids = list(map(lambda p: p.id_pedido, dia)) #Para iterar varias veces
    ventas = map(lambda p: (p.nombre.split("_")[0], p.cantidad), 
                 filter(lambda p: p.id_pedido in ids, generador_contenido_pedidos))
    diccionario = defaultdict(int) 
    for i in ventas:
        key = i[0]
        diccionario[key] += int(i[1])
    if diccionario:
        max_venta = max(diccionario.values())
        mas_vendida = {nombre for nombre, ventas in diccionario.items() if ventas == max_venta}
        return mas_vendida
    else:
        return set()

def pizza_del_mes(
        generador_pedidos: Generator,
        generador_contenido_pedidos: Generator,
        mes: str
        ) -> str:
    ids = {pedido.id_pedido for pedido in generador_pedidos if mes == pedido.fecha.split("-")[1]}
    pizzas = map(lambda p: (p.nombre.split("_")[0], p.cantidad), 
                 filter(lambda p: p.id_pedido in ids, generador_contenido_pedidos))
    diccionario = defaultdict(int)
    for key, value in pizzas:
        diccionario[key] += value
    if diccionario:
        max_cantidad = max(diccionario.values())
        pizza_mes = {nombre for nombre, ventas in diccionario.items() if ventas == max_cantidad}
        return pizza_mes
    else:
        return set()

def popularidad_mezcla_de_ingredientes(
        generador_pizzas: Generator,
        generador_contenido_pedidos: Generator,
        ingredientes: set
        ) -> int:
    pizzas = map(lambda p: (p.nombre, p.cantidad), generador_contenido_pedidos)
    ingredientes_p = map(lambda p: p.nombre,
                          filter(lambda x: set(x.ingredientes.split(";")) & ingredientes 
                                 == ingredientes, generador_pizzas)) #Intersección
    ingredientes_p = list(ingredientes_p)
    pizzas = map(lambda p: p[1], 
                 filter(lambda x: x[0] in ingredientes_p, pizzas))
    cantidad = 0
    for i in pizzas:
        cantidad += i
    return cantidad

def total_ahorrado_pedidos(
        generador_contenido_pedidos: Generator,
        generador_pizzas: Generator
        ) -> int:
    precio = map(lambda p: (p.nombre, p.precio), generador_pizzas)
    dic = defaultdict()
    for p in precio:
        dic[p[0]] = p[1]
    descuento = defaultdict(int)
    for pedido in generador_contenido_pedidos:
        if pedido.nombre in dic.keys():
            ahorro = float(dic[pedido.nombre] * pedido.cantidad)
            dscto = float(pedido.descuento)
            ahorro *= dscto
            descuento[pedido.id_pedido] += ahorro
    total = sum(descuento.values())
    return round(total)

def pizza_favorita_cliente(
        generador_pedidos: Generator,
        generador_contenido_pedidos: Generator,
        id_cliente: int,
        ) -> tuple:
    cliente = list(map(lambda p: p.id_pedido,
                   filter(lambda x: x.id_cliente == id_cliente, generador_pedidos)))
    pizzas = list([p.nombre.split("_")[0], p.cantidad] for p in generador_contenido_pedidos
               if p.id_pedido in cliente)
    nro_pizzas = Counter()
    for nombre, cantidad in pizzas:
        nro_pizzas[nombre] += cantidad
    if nro_pizzas:
        cantidad = max(nro_pizzas.values())
        tupla = list((picsa, venta) for picsa, venta in nro_pizzas.items() if venta == cantidad)
        tupla = tuple(tupla)
        return tupla
    else:
        return tuple()

# Consultas que ocupan 3 o mas Generadores

def local_mas_pizzas_vendidas_por_tipo_de_pizza(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        generador_locales: Generator,
        tipo_de_pizza: str
        ) -> Iterable:
    pizzas = map(lambda x: (x.id_pedido, x.cantidad) , 
                 filter(lambda p: p.nombre.split("_")[0] == tipo_de_pizza,
                     generador_contenido_pedidos))
    pizzas = list(pizzas)
    ids_pedidos = [x[0] for x in pizzas]
    ids_locales = list(map(lambda l: (l.id_local, l.id_pedido) ,
                           filter(lambda p: p.id_pedido in ids_pedidos, generador_pedidos)))
    ventas = defaultdict(int)
    for id_local, id_pedido in ids_locales:
        for pedido_id, cantidad in pizzas:
            if pedido_id == id_pedido:
                ventas[id_local] += cantidad
    if not ventas:
        return list()
    max_ventas = max(ventas.values())
    objetivo = [local for local, venta in ventas.items() if venta == max_ventas]
    locales = filter(lambda local: local.id_local in objetivo, generador_locales)
    return locales 

def ganancia_total_de_un_local(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        generador_pizzas: Generator,
        id_local: int
        ) -> int:
    precios = {p.nombre: p.precio for p in generador_pizzas}
    ganancias = defaultdict(int)
    for p in generador_contenido_pedidos:
        ganancias[p.id_pedido] += round(((precios[p.nombre]) * p.cantidad) * (1 - p.descuento))
    ganancia = 0
    for l in generador_pedidos:
        if l.id_pedido in ganancias.keys() and l.id_local == id_local:
                ganancia += ganancias[l.id_pedido]
    return round(ganancia)

def promedio_ventas_con_descuento_de_un_pais(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        generador_locales: Generator,
        pais: str
        ) -> float:
    dscto_pedido = {p.id_pedido: p.descuento for p in generador_contenido_pedidos}
    id_locales_pais = set(map(lambda l: l.id_local,
                          filter(lambda p: p.pais == pais, generador_locales)))
    promedio_dscto = float(0)
    n = 0
    for p in generador_pedidos:
        if p.id_pedido in dscto_pedido.keys() and p.id_local in id_locales_pais:
            promedio_dscto += dscto_pedido[p.id_pedido]
            n += 1
    if n:
        promedio_dscto = promedio_dscto/n
    return round(promedio_dscto, 2)

def gasto_cliente_por_mes(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        generador_pizzas: Generator,
        id_cliente: int,
        year: int,
        ) -> list:
    pedidos_cliente = list(map(lambda x: (x.id_pedido, int(x.fecha.split("-")[1])), 
                          filter(lambda p: p.id_cliente == id_cliente and
                                  int(p.fecha.split("-")[0]) == year, generador_pedidos)))
    gastos = defaultdict(int)
    precios = {p.nombre: p.precio for p in generador_pizzas}
    for p in generador_contenido_pedidos:
        for l in pedidos_cliente:
            if p.id_pedido == l[0]:
                gastos[l[1]] += (precios[p.nombre] * p.cantidad) * (1 - p.descuento)
    lista = [round(gastos[i]) for i in range(1, 13)]
    return lista

def pizzas_vendidas_mes_pais(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        generador_locales: Generator,
        pais: str,
        mes: int,
        year: int,
        ) -> int:
    paises = set(map(lambda x: x.id_local, filter(lambda l: l.pais == pais, generador_locales)))
    locales = list(map(lambda x: x.id_pedido, 
                      filter(lambda p: int(p.fecha.split("-")[1]) == mes and 
                             p.id_local in paises and 
                             int(p.fecha.split("-")[0]) == year, generador_pedidos)))
    cantidad = 0
    for p in generador_contenido_pedidos:
        for l in locales:
            if p.id_pedido == l:
                cantidad += p.cantidad
    return cantidad

# Consulta anidada

def consulta_anidada(instrucciones: dict) -> Any:
    consultas = [cliente_indeciso, pizzas_con_ingrediente, pizzas_pagables_de_un_tamano,
                 cantidad_empleados_pais, total_ahorrado_pedidos]
    cargas = [cargar_contenido_pedidos, cargar_locales, cargar_pedidos, cargar_pizzas]
    functions = {f.__name__: f for f in consultas}
    cargar = {f.__name__: f for f in cargas}
    for key, value in instrucciones.items():
        if type(value) == dict:
            generador = consulta_anidada(value)
            new = {key: generador}
            instrucciones.update(new)
    for key in instrucciones.keys():
        if key == 'funcion':
            funcion = instrucciones[key]
            if funcion in cargar.keys():
                funcion = cargar[funcion]
                return funcion(instrucciones['path'])
            elif funcion in functions.keys():
                funcion = functions[funcion]
                variables = {k: v for k, v in instrucciones.items() if k != 'funcion'}
                return funcion(**variables)
    return generador #Por si no hay nada o es solo de carga
