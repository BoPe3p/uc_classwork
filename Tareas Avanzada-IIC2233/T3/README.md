# Tarea 3: Little DCCaesars 🧟🍕

- Nombre: Rafael Ignacio Lorca Muñoz
- Sección: 3
- Usuario GitHub: BoPe3p

## Consideraciones generales :octocat:

Esta tarea consiste en correr el programa para llevar las cuentas de la renombrada franquicia Little DCCaesars, para esto es que se modifica el módulo principal del programa `consultas.py` en donde se implementan varias funciones que responden a varias preguntas que le surgen a los zombies con respecto a los datos que obtienen del manejo de la franquicia. De la carpeta data es que se obtiene toda la información de las *Pizzas* que se venden, los *Pedidos* y su *Contenido*, además de también los *Locales* exparcidos por todo el mundo. 

Dicho módulo se puede dividir en secciones. La primera parte tiene funciones que se encarga de **Cargar  datos**, la segunda parte que se encarga de filtrar las **consultas de un generador** y otras dos que se encargan de consultas de **dos o tres generadores**. Finalmente se aplica una función para responder a una **consulta anidada**, donde se puede necesitar de varias de las funciones antes implementadas, por lo que se pasa las instrucciones en formato de `dict`. 

La tarea fue realizada con python `3.11.9`.

## Cosas implementadas y no implementadas :white_check_mark: :x:

### Carga de datos: 8 pts (5%)
**cargar_pizzas()✅ :** Tests públicos ok.</p>
**cargar_localess()✅ :** Tests públicos ok.</p>
**cargar_pedidos()✅ :** Tests públicos ok.</p>
**cargar_contenido_pedidos()✅ :** Tests públicos ok.</p>

### Consultas de un generador: 42 pts (24%)
**pedidos_con_al_menos_esta_pizza()✅ :** Tests públicos ok.</p>
**cantidad_vendida_de_pizza_por_tipo()✅ :** Tests públicos ok.</p>
**pedido_con_mayor_descuento_utilizado()✅ :** Tests públicos ok.</p>
**ajustar_precio_segun_ingredientes()✅ :** Tests públicos ok.</p>
**clientes_despues_hora()✅ :** Tests públicos ok.</p>
**cliente_indeciso()✅ :** Tests públicos ok..</p>
**pizzas_con_ingrediente()✅ :** Tests públicos ok.</p>
**pizzas_pagables_de_un_tamano()✅ :** Tests públicos ok.</p>
**cantidad_empleados_pais()✅ :** Tests públicos ok.</p>

### Consultas de dos generadores: 54 pts (31%)
**ganancias_producidas_en_los_pedidos()✅ :** Tests públicos ok.</p>
**pizza_mas_vendida_del_dia()✅ :** Tests públicos ok.</p>
**pizza_del_mes()✅ :** Tests públicos ok.</p>
**popularidad_mezcla_de_ingredientes()✅ :** Tests públicos ok.</p>
**total_ahorrado_pedidos()✅ :** Tests públicos ok.</p>
**pizza_favorita_cliente()✅ :** Tests públicos ok.</p>

### Consultas de tres generadores: 62 pts (35%)
**local_mas_pizzas_vendidas_por_tipo_de_pizza()✅ :** Tests públicos ok.</p>
**ganancia_total_de_un_local()✅ :** Tests públicos ok.</p>
**promedio_ventas_con_descuento_de_un_pais()✅ :** Tests públicos ok.</p>
**gasto_cliente_por_mes()✅ :** Tests públicos ok.</p>
**pizzas_vendidas_mes_pais()✅ :** Tests públicos ok.</p>

### Consulta anidada: 9 pts (5%)
**consulta_anidada()✅ :** Tests públicos ok.</p>

## Ejecución :computer:
El módulo principal (y único) de la tarea a ejecutar es  ```consultas.py```.

## Librerías :books:
### Librerías utilizadas
La lista de librerías/módulos que utilicé fue la siguiente:

1. ```typing```: ```Any```, ```Generator``` y ```Iterable```
2. ```functools```: ```reduce```
3. ```itertools```: ```tee```, ```islice```, ```chain``` y ```cycle```
4. ```collecions```: ```defaultdict``` y ```Counter```

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Se supone que el path entregado para cargar los datos son correctos y funcionan bien, debido a que no especifica que se tenga que hacer un chequeo de los path en el enunciado, solo hice la función que devuelve un generador con los namedtuples.

2. En general, siguiendo con lo anterior, se espera que cuando se tiene que recibir por ejemplo el nombre de una pizza, si está mal escrito no se tenga que revisar si fue un error de tipeo o algo por el estilo, tambipen que se respete el tipo de los argumentos que se reciben (str, int, float) en las funciones que en el enunciado se especifica el tipo.

3. En la parte de consulta anidada, realicé el código antes de una forma en que no importaba el nombre de la llave del diccionario, sino que tomaba los valores después de la llave 'funcion', los pasaba a una lista y los desempaquetaba, sin embargo al no pasar todos los test cases, cambié la aproximación a un desempaquetado por palabra clave (kwargs) es por esto que un supuesto es que los nombres de las llaves van a respetar (ser los mismos) que los nombres de las variables de las funciones.

## PD:
**Corrí el código varias veces y siempre pasaba los test cases, habían algunas veces que me daba error en el tiempo de la carga de datos, pero debería funcionar el 90% de las veces (sirve más si no se minimiza la ventana de cmd o gitbash, no sé por qué)**
:) 
-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<[link de código](https://stackoverflow.com/questions/4945155/how-to-clone-a-generator-object)>: El código \<clona un generador> y está implementado en el archivo <consultas.py> en la linea <67> y <lo utilizo porque al calcular el máximo descuento el generador se consume y necesitaba iterar nuevamente sobre él>.

2. \<[link de código](https://docs.python.org/3/library/itertools.html)>: En la función cliente_indeciso (linea 95) utilizo varias funciones de itertools que no están presentes en los contenidos del syllabus. Por ejemplo: tee que \<clona un generador>, islice que <es equivalente al slicing en generadores>, chain que <une dos generadores> y cycle que <crea un bucle de un generador para iterar sobre él>. En esta función tambien usé código de: \<[link de código](https://stackoverflow.com/questions/571850/adding-elements-to-python-generators)> y de \<[link de código](https://stackoverflow.com/questions/34732311/how-to-slice-a-generator-object-or-iterator)>.

3. \<[link de código](https://www.geeksforgeeks.org/defaultdict-in-python/)>: Igual que lo anterior, no caque código en sí de esta página, pero sí la utilizo para comprender mejor el uso de defaultdict. Utilizo estos conocimientos por primera vez en la fundión ganancias_producidas_en_los_pedidos (línea 134) y en general utilizo defaultdict para guardar ints por llaves y poder sumarle a dichos valores.

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).