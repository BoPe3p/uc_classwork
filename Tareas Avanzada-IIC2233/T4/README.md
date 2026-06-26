# Tarea 4: DCComparte Archivos 💻🍃

- Nombre: Rafael Ignacio Lorca Muñoz
- Sección: 3
- Usuario GitHub: BoPe3p

## Consideraciones generales :octocat:

Esta tarea consiste en correr en un computador (o terminal claramente) `main.py` desde la carpeta del Servidor para abrir DCComparte_Archivos. Luego, distintos usuarios se podrán conectar al servidor siempre y cuando se conecten a su mismo puerto ara así poder recibir los conocimientos del profesor Hernán. Esribiendo en la consola el siguiente argumento:`py main.py port`, donde port es un numero, se puede hacer networking para empezar a compartir archivos. 

La tarea fue realizada con python `3.11.9`.

### Cosas implementadas y no implementadas :white_check_mark: :x:

Perdón por no hacerlo en el formato esperado pero como hice tan poco voy a señalar las cosas que se pueden hacer con mi código: Se puede entrar con varios usuarios al servidor y muestra en una pantalla tanto los archivos en el servidor como los usuarios conectados. Solo se pueden conectar los que pasan los filtros señalados en el enunciado y cuando un usuario se desconecta se printea en la terminal del servidor la desconexión. Se miplementan varias funciones para enviar archivos pero lamentablemente me quede sin el tiempo para hacer eso :(, lo mismo para la conversación entre clientes.

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py``` de cada carpeta. Además se crearon los siguientes archivos y directorios adicionales que encontrarán en ```BoPe3p-iic2233-2024-2\Tareas\T4\``` (Repositorio personal de GitHub).:

1. ```server```  y ```cliente``` son las carpetas que contienen al cliente y al servidor.
2. ```server\main.py``` contiene la clase Server.
3. ```cliente\main.py``` contiene la clase DCComparte_Archivos que se encarga de crear al cliente y de la intefaz gráfica.
4. ```cliente\backend\cliente.py``` contiene la clase Client.
5. ```cliente\frontend\login_window.py``` contiene la clase Ventana_login que es la interfaz de login de los clientes.
6. ```cliente\frontend\main_window.py``` contiene las clases Ventana_Descargas y Ventana_Archivos que son las ventanas que se ven en DCComparte_Archivos.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías/módulos que utilicé fue la siguiente:

1. ```sys```: ```sys.argv```
2. ```os```: ```os.path.join```, ```os.path.exists```, ```os.listdir```, etc
3. ```threading```: ```random.randint```
4. ```PyQt5.QtCore```: ```Qt``` y ```pyqtSignal```
5. ```PyQt5.QtWidgets```: Para varios widgets
6. ```PyQt5.QtGui```: ```QIcon```
7. ```json``` : ```loads``` y ```dumps```
8. ```socket```: Para todo lo relacionado con networking

**PD: Por lo menos, quisiera recalcar que a mi solo me servía el comando: 'py main.py' para correr el archivo. Algunos prints no van con tildes para prevenir el printeo de caracteres inválidos.**

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<[link](https://www.pythontutorial.net/pyqt/pyqt-qmainwindow/)>: Este \<explica varias funcionalidades de PyQt QMainWindow. > Implementé las mencionadas en <main_window.py> para hacer la ventana de descargas y la ventana mis archivos.

2. \<[link](https://www.pythontutorial.net/pyqt/pyqt-qgridlayout/)>: Este \<explica varias funcionalidades de PyQt QGridLayout. > Implementé las mencionadas en <main_window.py> para hacer el main_layout de la ventana de descargas (linea 48).

3. \<[link](https://doc.qt.io/qt.html#qtforpython)>: Esta es la documentación de PyQt \<Lo utilicé principalmente para buscar widgets que podrían serme útiles para la ventana de descargas y de mis archivos. > También encontré widgets en: <[link](https://www.pythonguis.com/tutorials/pyqt-basic-widgets/#qlistwidget)>. Implementé las mencionadas en <main_window.py> y de esta página saqué widgets como: qlistwidget, qtablewidget, qprogressbar.

4. Utilicé varios scripts de contenidos, especialmente para el servidor y el cliente, estos son: \<De la semana 11: Networking-ejemplos para el el servidor que se conecta a varios clientes, por ejemplo en la parte en que se asigna para cada cliente un thread de escuchar línea 59 de mi módulo servidor\main. Otro script fue el de la semana 14: pyqt-networking\_ejemplo_avanzado en donde también ocupo la idea de hacer un QThread para el cliente que (en mi caso) se encargue de manejar las descargas del cliente.>. Igualmente me informé sobre algunos métodos que se utilizaban en dichos scripts como cuando hacen que el comando para enviar información del servidor sea un staticmethod de esta página: <[link]https://www.geeksforgeeks.org/python-staticmethod-function/>, al final lo que hace es que no se necesite instanciar (en este caso el método send) con la clase servidor. 

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).
