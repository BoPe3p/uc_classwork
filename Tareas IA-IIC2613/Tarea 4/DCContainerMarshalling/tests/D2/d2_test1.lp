% ═══════════════════════════════════════════
% D2 Test 1: Generación de movimientos
% 2 stacks, 3 containers
% Container 2 está cubierto, solo 3 se debe mover sobre 1 y volver a su posición inicial
% ═══════════════════════════════════════════
#const bound=2.

stack_base(b1; b2).
container(1..3).

on(2, b1, 0).
on(1, 2, 0).
on(3, b2, 0).