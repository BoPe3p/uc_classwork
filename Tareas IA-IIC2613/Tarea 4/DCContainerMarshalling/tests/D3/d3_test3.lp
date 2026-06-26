% ═══════════════════════════════════════════
% D3 Test 3: 3 stacks, 6 contenedores
% Todas las pilas desordenadas
% ═══════════════════════════════════════════
#const bound=10.
#const hlim=4.

stack_base(b1; b2; b3).
container(1..6).

on(3, b1, 0).
on(6, 3, 0).
on(1, b2, 0).
on(5, 1, 0).
on(2, b3, 0).
on(4, 2, 0).
