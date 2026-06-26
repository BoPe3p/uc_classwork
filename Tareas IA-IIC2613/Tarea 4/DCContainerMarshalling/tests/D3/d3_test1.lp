% ═══════════════════════════════════════════
% D3 Test 1: Ya ordenado (trivial)
% Expected: SATISFIABLE con 0 moves
% ═══════════════════════════════════════════
#const bound=0.
#const hlim=3.

stack_base(b1; b2).
container(1..4).

on(4, b1, 0).
on(2, 4, 0).
on(1, 2, 0).
on(3, b2, 0).
