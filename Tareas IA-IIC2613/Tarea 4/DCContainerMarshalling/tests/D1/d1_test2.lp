% ═══════════════════════════════════════════
% D1 Test 2: Multiple pasos + inertia
% 3 stacks, 3 containers, 2 movimientos
% Debería mover el container 1 desde el suelo a 3 y luego de 3 a 2
% ═══════════════════════════════════════════
#const bound=2.

stack_base(b1; b2; b3).
container(1..3).

on(3, b1, 0).
on(2, b2, 0).
on(1, b3, 0).

move(1, 3, 0).   % T=0: Mover 1 a 3
move(1, 2, 1).   % T=1: Mover 1 a 3