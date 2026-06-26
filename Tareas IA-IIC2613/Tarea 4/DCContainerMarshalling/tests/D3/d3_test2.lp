% ═══════════════════════════════════════════
% D3 Test 2: Bahía desordenada
% 3 stacks, 4 containers, necesitan ordenarse en cada columna
% ═══════════════════════════════════════════
#const bound=2.
#const hlim=3.

stack_base(b1; b2; b3).
container(1..4).

on(3, b1, 0).
on(4, 3, 0).
on(2, b2, 0).
on(1, 2, 0).
