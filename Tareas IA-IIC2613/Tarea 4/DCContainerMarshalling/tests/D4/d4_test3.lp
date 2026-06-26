% ═══════════════════════════════════════════
% D4 Test 3: No-paralelismo drop+move
% Una pila desordenada + 1 arrival.
% En el mismo tiempo no pueden ocurrir drop y move.
% Expected: SATISFIABLE (Clingo encuentra la secuencia correcta)
% ═══════════════════════════════════════════
#const bound=6.
#const hlim=3.

stack_base(b1; b2).
container(3).

% b1 tiene solo container 3
on(3,b1,0).

% Container 1 llega en T=1, container 2 en T=2
arrive(1,1).
arrive(2,2).
