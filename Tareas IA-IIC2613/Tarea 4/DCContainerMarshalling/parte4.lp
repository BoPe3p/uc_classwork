% ============================================================
% DESAFIO 4: DCContainer Marshalling completo
% ============================================================

% Dominio temporal
tiempo(0..bound).

% Activamos el arrive
% Los containers que llegan mediante arrive también son containers
container(C) :- arrive(C,T), tiempo(T), T < bound.

% Parte 1: dinámica para el predicado on 

% Efecto positivo de move: C1 pasa a estar sobre C2 en T+1
on(C1,C2,T+1) :- move(C1,C2,T), T < bound.

% Efecto positivo de drop: C queda sobre el tope de la pila de base B en T+1
on(C,X,T+1) :- drop(C,B,T), tope(B,X,T), T < bound.

% Inercia: on persiste si C1 no fue movido en este paso de tiempo
on(C1,C2,T+1) :- on(C1,C2,T), not move(C1,_,T), T < bound.

% Parte 2: precondiciones de move

% Un container está en el patio si tiene una posición on definida
en_patio(C,T) :- on(C,X,T), container(C), tiempo(T).

% Un container/base está ocupado si tiene algo directamente encima
ocupado(C,T) :- on(X,C,T), container(X).

% Libre: en el patio y sin nada encima
libre(C,T) :- en_patio(C,T), not ocupado(C,T).

% Destinos válidos:
% 1. Base vacía (nada directamente encima): permite poner un container al fondo de pila vacía
% 2. Container libre en el patio: permite apilar encima

valido(D,T) :- stack_base(D), tiempo(T), not ocupado(D,T).
valido(D,T) :- libre(D,T).

% Precondición: solo mover containers que estén libres en el patio
:- move(C1,C2,T), not libre(C1,T), tiempo(T), T < bound.

% Precondición: solo mover hacia destinos válidos
:- move(C1,D,T), not valido(D,T), tiempo(T), T < bound.

% Precondición: no se puede mover un container sobre sí mismo
:- move(C1,C2,T), C1 = C2.

% Parte 3: Encontrando soluciones

% Definimos la altura máxima
hmax(hlim).

% Base: las bases de pila tienen altura 0
altura(B,0,T) :- stack_base(B), tiempo(T).
% Altura de cada posición acotada por hmax
altura(C1,H+1,T) :- on(C1,C2,T), altura(C2,H,T), tiempo(T), hmax(Max), H < Max.

% No mover a una pila que ya alcanzó la altura máxima
:- move(C1,C2,T), altura(C2,H,T), hmax(Max), H >= Max.

% Desordenado: un container de mayor número está directamente sobre uno de menor número.
desordenado(T) :- on(C1,C2,T), container(C1), container(C2), C1 > C2.
ordenado(T) :- tiempo(T), not desordenado(T).

% Todos los containers que llegan deben estar en el patio al final
:- arrive(C,T), tiempo(T), not en_patio(C,bound).

% Todas las pilas deben estar ordenadas al final del horizonte
:- not ordenado(bound).

% ============================================================
% Parte 4: Llegada dinámica de containers
% ============================================================

% available(C,T): container C ya llegó al área adyacente para ingresar al patio
available(C,T) :- arrive(C,T).
available(C,T+1) :- available(C,T), not dropped(C,T), T < bound.
dropped(C,T) :- drop(C,B,T), stack_base(B).

% Tope de cada pila: lugar donde se dropean los containers.
% Si la pila está vacia se dropea en la base.
% Si tiene containers, el tope es el container libre.
en_pila(C1,B,T) :- on(C1,B,T), stack_base(B), container(C1).
en_pila(C1,B,T) :- on(C1,C2,T), en_pila(C2,B,T), container(C1).

apilado(B,T) :- en_pila(C,B,T).
tope(B,B,T) :- stack_base(B), tiempo(T), not apilado(B,T).
tope(C,B,T) :- stack_base(B), en_pila(C,B,T), libre(C,T).

% No se puede hacer drop a una pila que ya alcanzó la altura máxima
:- drop(C,B,T), tope(B,X,T), altura(X,H,T), hmax(Max), H >= Max.

% Solo se puede dropear containers que estén disponibles
:- drop(C,B,T), not available(C,T).

% FIFO: no se puede ingresar C2 si hay algún C1 que llegó antes y sigue esperando
:- drop(C2,_,T), available(C1,T), arrive(C1,T1), arrive(C2,T2), T1 < T2, C1 != C2.

% No paralelismo: drop y move no pueden ocurrir en el mismo paso de tiempo
:- move(_,_,T), drop(_,_,T).

% GENERACIÓN DE ACCIONES

% A lo sumo 1 move por paso: solo containers libres en el patio, destinos válidos
{ move(C1,C2,T) : libre(C1,T), valido(C2,T), C1 != C2 } 1 :- tiempo(T), T < bound.

% A lo sumo 1 drop por paso: solo containers disponibles, hacia bases de pila
{ drop(C,B,T) : available(C,T), stack_base(B) } 1 :- tiempo(T), T < bound.