% ═══════════════════════════════════════════
% D3 Test 4: Restricción hmax activa
% 3 containers en una sola pila, hmax=2.
% La única pila libre (b2) tiene hmax=2, así que no se puede
% mover el container del fondo sin violar la altura si b2 ya tiene algo.
% Se requiere usar b3 como auxiliar.
% Expected: SATISFIABLE (solución en <= 5 pasos)
% ═══════════════════════════════════════════
#const bound=5.
#const hlim=2.

stack_base(b1; b2; b3).
container(1..3).

% Pila b1 desordenada: 3 sobre 2 sobre 1 (de arriba a abajo = 3,2,1 -> desordenado)
on(1,b1,0).
on(2,1,0).
on(3,2,0).
