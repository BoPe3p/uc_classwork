% ═══════════════════════════════════════════
% D1 Test 2: Multiple pasos + inertia
% 3 stacks, 3 containers, 1 movimientos
% Debería mover el container 1 a b2 (mismo espacio que el container 2)
% Debería dar SATISFIABLE porque aún no se implementa restricción de espacio
% Recomendamos corroborar con logs de clingo, el visualizador debería bugearse
% ═══════════════════════════════════════════
#const bound=1.

stack_base(b1; b2; b3).
container(1..3).

on(3, b1, 0).
on(2, b2, 0).
on(1, b3, 0).

move(1, b2, 0).