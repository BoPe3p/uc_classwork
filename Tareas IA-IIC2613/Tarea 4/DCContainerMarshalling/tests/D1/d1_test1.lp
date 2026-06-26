% ═══════════════════════════════════════════
% D1 Test 1: Inercia básica
% 2 stacks, 3 containers, 1 move manual
% Debería mover el container 1 de una columna a otra
% ═══════════════════════════════════════════
#const bound=1.

stack_base(b1; b2).
container(1..3).

on(2, b1, 0).
on(1, 2, 0).
on(3, b2, 0).

% Mover container 1 de encima de 2 a encima de 3
move(1, 3, 0).
