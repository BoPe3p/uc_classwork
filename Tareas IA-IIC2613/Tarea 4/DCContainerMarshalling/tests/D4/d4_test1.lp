% ═══════════════════════════════════════════
% D4 Test 1 (Bonus): containers que llegan
% 3 stacks, 4 containers iniciales + 2 arrivals
%
% Arrivals:
%   Container 5 arrives at T=2
%   Container 1 arrives at T=3
%
% Debe terminar con 7 contianers ordenados en las columnas
% Solución óptima (FIFO + minimize): 5 acciones, en 7 tiempos
% ═══════════════════════════════════════════
#const bound=8.
#const hlim=3.

stack_base(b1; b2; b3).
container(2..4).

on(4, b1, 0).
on(2, 4, 0).
on(3, b2, 0).

arrive(5, 2).
arrive(1, 3).
arrive(7, 4).
arrive(6, 5).
