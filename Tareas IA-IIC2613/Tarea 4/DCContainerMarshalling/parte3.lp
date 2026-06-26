% ============================================================
% DESAFIO 1: dinámica para el predicado on con respecto a move
% definimos el dominio del tiempo T: 
tiempo(0..bound).

% Efectos positivos de cada acción
on(C1,C2,T+1) :- move(C1,C2,T), T < bound.

% Efectos negativos: persistencia
on(C1,C2,T+1) :- on(C1,C2,T), not move(C1,_,T), T < bound.
% ============================================================
% DESAFIO 2: Diseñar precondición de move
% Tenemos que idear la representación de los bloques libres

% Un bloque está libre si no hay otros encima de él
libre(C1,T) :- container(C1), tiempo(T), not ocupado(C1,T).
ocupado(C1,T) :- on(C2,C1,T), container(C2).

% Vemos las restricciones para movimientos inválidos

% Se puede mover solo containers libres
:- move(C1,C2,T), ocupado(C1,T), tiempo(T), T < bound.

% Un container no puede posicionarse sobre otro que no esté en el tope de una pila
% el tope es el bloque que definimos como libre
% también se puede poner directamente sobre una base

valido(D,T) :- stack_base(D), tiempo(T).
valido(D,T) :- libre(D,T), container(D).

:- move(C1,D,T) , not valido(D,T), tiempo(T), T < bound.
% ============================================================

% DESAFIO 3: Encontrando soluciones

% Activamos a hmax
hmax(hlim).

% 1. Restricción de altura máxima permitida
% Base: las bases de pila tienen altura 0
altura(B,0,T) :- stack_base(B), tiempo(T).
% Recursión acotada por hmax
altura(C1,H+1,T) :- on(C1,C2,T), altura(C2,H,T), tiempo(T), hmax(Max), H < Max.

% Prohibición de altura. 
:- move(C1,C2,T), altura(C2,H,T), hmax(Max), H >= Max.

% 2. Definir ordenado(T): ascendente de arriba hacia abajo.
% Si C1 está sobre C2 y C1 > C2, la pila está desordenada.
desordenado(T) :- on(C1,C2,T), container(C1), container(C2), C1 > C2.

ordenado(T) :- tiempo(T), not desordenado(T).

% 3. Restricción para encontrar soluciones:
:- not ordenado(bound).

% Generación de movimientos: como máximo 1 acción por tiempo
{ move(C1,C2,T) : container(C1), valido(C2,T) } 1 :- tiempo(T), T < bound.