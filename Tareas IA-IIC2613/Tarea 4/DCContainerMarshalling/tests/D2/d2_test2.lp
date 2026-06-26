% ═══════════════════════════════════════════
% D2 Test 2: 3 stacks, 5 containers
% Verificar que solo se muevan containers en el top
% ═══════════════════════════════════════════
#const bound=3.

stack_base(b1; b2; b3).
container(1..5).

on(4, b1, 0).
on(2, 4, 0).
on(5, b2, 0).
on(3, 5, 0).
on(1, 3, 0).

move(1,2,1).