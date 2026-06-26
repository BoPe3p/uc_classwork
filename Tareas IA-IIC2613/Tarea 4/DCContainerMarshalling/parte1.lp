% DESAFIO 1: dinámica para el predicado on con respecto a move
% definimos el dominio del tiempo T: 
tiempo(0..bound).

% Efectos positivos de cada acción
on(C1,C2,T+1) :- move(C1,C2,T), T < bound.

% Efectos negativos: persistencia
on(C1,C2,T+1) :- on(C1,C2,T), not move(C1,_,T), T < bound.
