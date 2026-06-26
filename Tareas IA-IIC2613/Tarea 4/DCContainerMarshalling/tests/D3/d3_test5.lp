% ═══════════════════════════════════════════
% D3 Test 5: UNSATISFIABLE — desordenado y sin movimientos posibles
% bound=0: ningún move es posible (T < 0 es siempre falso).
% El estado inicial ya tiene 3 sobre 1 (3>1 → desordenado).
% Como no hay tiempo para corregirlo, el sistema debe dar UNSAT.
% Expected: UNSATISFIABLE
% ═══════════════════════════════════════════
#const bound=1.
#const hlim=2.

stack_base(b1;b2).
container(1..4).

% b1: 3 sobre 1 — desordenado (3 > 1)
on(1,b1,0).
on(3,1,0).

% b2: 2 solo — ordenado
on(2,b2,0).
on(4,2,0).
