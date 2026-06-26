% ═══════════════════════════════════════════
% D2 Test 3: Movimiento inválido (container tapado)
% Container 1 está tapado por container 2.
% Intentar mover 1 en T=0 debe dar UNSATISFIABLE.
% ═══════════════════════════════════════════
#const bound=1.

stack_base(b1; b2).
container(1..3).

on(1,b1,0).
on(2,1,0).   % 2 tapa a 1 -> 1 no está libre
on(3,b2,0).

% Mover 1 con algo encima es inválido
move(1,3,0).
