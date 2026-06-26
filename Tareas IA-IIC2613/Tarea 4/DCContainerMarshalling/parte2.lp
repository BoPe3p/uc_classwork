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

valido(D,T) :- stack_base(D), tiempo(T), not ocupado(D,T).
valido(D,T) :- libre(D,T).

:- move(C1,D,T) , not valido(D,T), tiempo(T), T < bound.