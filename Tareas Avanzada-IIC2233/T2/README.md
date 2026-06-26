# Tarea 2: DCCampesino 🌻🧟

- Nombre: Rafael Ignacio Lorca Muñoz
- Sección: 3
- Usuario GitHub: BoPe3p

## Consideraciones generales :octocat:

Esta tarea consiste en correr el juego DCCultivo en `main.py`, nuestro principal archivo. A pedido del profe Hernán, esribiendo en la consola el siguiente argumento:`python3.11 main.py nombre_jardin dificultad`, donde nombre_jardin es el jardín con el que se accede a DCCampesino y dificultad, es la dificultad en la cual simulas un día en el jardín. Tendrás un total de 7 días (sin contar el día 0 y el día 8, donde igualmente no se pueden hacer acciones) para juntar el número máximo de soles, para esto con el código se puede cultivar plantas, crear plantas mutantes en un laboratorio y cuidar el jardín para prepararte para las hordas de zombies y las heladas. 

Otros archivos importantes para esta tarea son:`dccampesino.py` y `dccampesino2.py` en donde se pueden encontrar las clases `Jardin` y `Plantas` respectivamente, la última mencionada es una clase *abstracta* de la cual salen el resto de plantas creadas. En el archivo `parametros.py` se encuentran los PARÁMETROS, que son constantes que modifican algunas variables y son útiles para el código, `extras.py` es un archivo con la función que implementé para leer los archivos de la carpeta **data**, varios *f-strings* con los menús y la función `menu_lab2` que utilizo para devolver una parte del menú del laboratorio. Finalmente, el archivo `dia.py` tiene la función pasar_dia que es la encargada de simular todos los eventos y posibilidades del código.

Sobre esta última parte, primero se inicia en el día 0 en donde solamente se puede ver el jardín, se **setea** una **temperatura** entre la mínima (-5) y la máxima (25), estos valores se mantienen solamente si el evento que ocurre durante el día es una oleada de zombies. Luego, se actualiza esta temperatura para las plantas y se **aplican buffs/debuffs**, en particular se buscan si hay algún `Aresauce` o `Fensaulantro` en el tablero y también se sacan los buffs aplicados anteriormente por si los potenciadores murieron después de un ataque. Seguido ocurre un **evento** con una probabilidad que depende de la dificultad entregada, si ocurre una helada o un día tranquilo (sin eventos), se actualiza la temperatura, sino, una horda de zombies ataca el jardín. Se **calculan** los soles producidos/robados y **llegan plantas** nuevas al inventario de plantas para que podamos plantar o crear mutantes. Finalmente se **presenta el jardín** y uno puede **realizar acciones** para prepararse para el siguiente día.

La tarea fue realizada con python `3.11.9`.

## Cosas implementadas y no implementadas :white_check_mark: :x:

### Programación Orientada a Objetos: 16 pts (10%)
**✅ Definición de clases, herencia y *properties*:** Se aplica Multi Herencia, clases abstractas y se incluyen properties.</p>

### Preparación del programa: 6 pts (4%)
**✅ Inicio de la partida:** Se utiliza de forma correta sys.argv. Se inicia con los parámetros pedidos.</p>

### Entidades: 64 pts (39%)
**✅ Jardín:** Se implementan todos los métodos pedidos y se crean unos extras.</p>
**✅ Plantas:** Se implementan todas las plantas pedidas y sus respectivas funciones. </p>

### Flujo del programa: 40 pts (24%)
**✅ Menú de Inicio:** Todo ok.</p>
**✅ Menú Jardín:** Todo ok.</p>
**✅ Laboratorio:** Todo ok.</p>
**✅ Fin del juego:** Se hace lo pedido.</p>
**✅ Robustez:** A prueba de todo lo que se intentó.</p>

### Simular día: 23 pts (14%)
**✅ Temperatura:** Se hace lo pedido. (Ver @property congelacion y get_temp en dccampesino2.py).</p>
**✅ Eventos:** Oleada de Zombies y Helada implementados, también se añadío algunos parámetros para el día tranquilo (sin eventos).</p>
**✅ Calcular soles:** Se hace lo pedido.</p>
**✅ Llegada de plantas:** Se hace lo pedido.</p>
**✅ Presentación:** Se hace lo pedido.</p>

### Archivos: 15 pts (9%)
**✅ Archivos.txt:** Se trabaja correctamente con los archivos, la función que trata con ellos se puede encontrar en `extras.py`.</p>
**✅ parametros.py:** Parámetros bien definidos.</p>

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se crearon los siguientes archivos y directorios adicionales que encontrarán en ```BoPe3p-iic2233-2024-2\Tareas\T2\``` (Repositorio personal de GitHub).:

1. ```dccampesino.py```  y ```dccampesino2.py```para las clases.
2. ```extras.py``` para algunas funciones y para imprimir los menús.
3. ```dia.py``` para simular el paso del día.
4. ```parametros.py``` para los parámetros.

## Librerías :books:
### Librerías utilizadas
La lista de librerías/módulos que utilicé fue la siguiente:

1. ```sys```: ```sys.argv```
2. ```os```: ```os.path.join``` y ```os.path.exists```
3. ```random```: ```random.randint```
4. ```abc```: ```ABC``` y ```abstractmethod```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```get_ruta```: Hecha para **leer los archivos en la carpeta data y devolver una lista con eventos, plantas o jardines**.
2. ```pasar_dia```: Hecha para **Simular el paso del día, primero setea una nueva temperatura, luego selecciona un evento, después se calculan los soles, llegan plantas y finalmente printea el jardin**. Devuelve un "1" lo que se suma al día.
3. ```menu_lab2```: Hecha para **devolver el número exácto de plantas disponibles para mutar y tambien el número de plantas mutadas en formato f-string**.
4. ```get_temp```: Hecha para **actualizar continueament la temperatura del jardin como un atributo de propio de la planta**. Sirve para ver si la planta está congelada.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Supongo que los archivos de texto en la carpeta data pueden ser modificados a la hora de que se corra el código, en realidad no cambia mucho el código pero es válido si es que se quiere corregir con una mayor rigurosidad. Es por esto mismo que se supone que se seguirá el formato de los archivos entregados si es que se llegan a modificar y que no se pueden subir archivos vacíos.

2. El juego termina cuando el dia en el que uno está supera el parámetro de DURACION o también si es que se sale desde el menú inicial, en cualquiera de los casos para la siguiente partida no se guardan los datos, si uno sale desde el menú no se puede volver al día en el que estabas antes.

3. Con respecto al día, se parte en el día 0, el cual es considerado un día tranquilo y se pueden realizar todas las acciones (claramente no se puede plantar ya que el inventario está vacío). Los eventos empiezan cuando se pasa al día 1.

4. Sobre regar, quería hacer un número de intentos para regar dependiendo de la dificultad, pero se me complicó implementar eso a si que como no lo especifican, implementé que cada vez que se regara se gasten 10 soles (Sino se podría regar infinitamente sin penalización).

5. Al momento de iniciar se respetará el formato especificado por el enunciado: "python main.py nombre_jardin dificultad". El supuesto que hago es que el usuario tiene que entregar 3 argumentos, pero el primero siempre será main.py, los otros se puede equivocar, y el código está preparado para eso.

6. Cuando se cultiva una planta, aunque el jardín esté a una temperatura menor a la que esa planta soporta, no se congela. Sería raro que se congelara al instante. También, las plantas congeladas no pueden producir soles/potenciar la producción de estos. Eso sí, solamente por estar en el tablero, Fensaulantro y Aresauce si aplican sus buffs/debuffs respectivos. Por último, Potencilantro y Fensaulantro solo pueden potenciar Solaretillos, pero Cilantrillo puede potenciar Solaretillos, Cilantrillos y Aresauces. Los potenciadores no se stackean.

**PD: Por lo menos, quisiera recalcar que a mi solo me servía el comando: 'py main.py' para correr el archivo. Algunos prints no van con tildes para prevenir el printeo de caracteres inválidos.**

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<[link stackoverflow](https://stackoverflow.com/questions/43227103/nested-list-to-dict)>: Este \<sirve para definir un diccionario de una nested list, no utilicé el código en sí pero saqué algunas ideas de aquí. > Implementé las mencionadas en <extras.py> en la línea <77> para hacer <un diccionario con los stats de las plantas y así acceder a ellos de forma más facil cuando se defina el un objeto que nace de la clase Plantas>.

2. \<[link geeksforgeeks](https://www.geeksforgeeks.org/how-to-use-sys-argv-in-python/)>: Nos pidieron en el enunciado que investigáramos sobre la librería sys y como utilizar sys.argv, de esta página basé mi código. Se puede encontrar en el archivo `main.py` en la línea <13> para tomar un argumento que escribe el usuario en la consola.

3. Reutilicé código de la T1 aplicado a el contexto de esta tarea, pero la forma que definí el método 'regar' de esa tarea, lo encontré muy parecido a como potencian los potenciadores de la tarea, claramente le hice una mejora para ahorrar líneas. Se puede encontrar en el archivo `dccampesino.py` en la línea <343>.

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).