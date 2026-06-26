# Tarea 1: DCCultivo 🌱💧

- Nombre: Rafael Ignacio Lorca Muñoz
- Sección: 3
- Usuario GitHub: BoPe3p

## Consideraciones generales :octocat:

Esta tarea consiste de dos archivos importantes: `dccultivo.py` y `main.py`. El primer archivo contiene todas las funciones relacionadas con el mantenimiento del huerto del profesor Hernán. Con este archivo se pueden acceder a dos objetos `Predio` y `DCCultivo`. El primero entrega la posibilidad de crear planos de riego y de cultivos, plantar cultivos a elección, regarlos y eliminar un cultivo si es que se encuentra una plaga. El segundo nos permite crear predios para plantar y regar y cuenta con métodos para determinar si es posible regar o plantar cultivos en un plano o también detectar plagas que servirán para mantener los cultivos. 

El segundo archivo es un menú con el cual se puede interactuar con las funciones implementadas en dccultivo.py. La tarea fue realizada con python `3.11.9`.

### Cosas implementadas y no implementadas :white_check_mark: :x:

### Automatización DCCultivo: 36 pts (60%)
**✅ Predio crear_plano:** Realizado, tests públicos OK!</p>
**✅ Predio plantar:** Realizado, tests públicos OK!</p>
**✅ Predio regar:** Realizado, tests públicos OK!</p>
**✅ Predio eliminar_cultivo:** Realizado, tests públicos OK!</p>
**✅ DCCultivo crear_predios:** Realizado, tests públicos OK!</p>
**✅ DCCultivo buscar_y_regar:** Realizado, tests públicos OK!</p>
**✅ DCCultivo detectar_plagas:** Realizado, tests públicos OK!</p>
**✅ DCCultivo buscar_y_plantar:** Realizado, test públicos fáciles y difíciles OK! </p>

### Menú: 17 pts (28,3%)
**✅ Consola** Completo!</p>
**✅ Menú de Inicio** Completo!</p>
**✅ Menú de Acciones** Completo! </p>

### Aspectos Generales: 7 pts (11,7%)
**✅ Modularización**</p>
**✅ PEP8**</p>


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Desde aquí se puede acceder a un menú para interactuar con DCCultivo. Además se modificó el siguiente archivo:
1. ```dccultivo.py``` en ```BoPe3p-iic2233-2024-2\Tareas\T1\``` (Repositorio personal de GitHub).


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```path.join()```,```path.exists()```

### Librerías y fuciones propias
Por otro lado, creé varias funciones que son utilizadas en el archivo `main.py`:

1. ```Funciones de acción```: Para el menú, preferí definir una función para cada acción posible que requiera el uso de una función definida en `dccultivo.py`, estas funciones son --> `ver_predio()`,`plantar_cultivo()`, `regar_cultivo()` y `terminator_cultivo()`. Estas funciones en general imprimen un mini menú y le piden al usuario inputs para poder llamar a las funciones implementadas en `dccultivo.py`.

2. ```ordenar()```: Como bien dice el nombre, hice esta funció para ordenar una lista, específicamente en la función de `dccultivo.py`: `detectar_plagas()`. Esta función recibe la lista para ordenar y nos devuelve la tupla: lista[1], lista[0]. El primer elemento equivale al número de espacios eliminados del predio por la función y el segundo el código del predio.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos realizados son los especificados por la tarea, especificamente aquellos relacionados con los inputs que se tenían que pedir en `main.py`.

-------
