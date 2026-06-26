% ═══════════════════════════════════════════
% D4 Test 2: FIFO estricto con esperas
% 2 stacks vacíos + 1 pila, 3 arrivals.
% Los arrivals llegan uno por uno y deben ingresarse en orden.
% Contenedores: 1 llega en T=1, 3 en T=2, 2 en T=3.
% FIFO: primero 1, luego 3, luego 2.
% Al final las pilas deben estar ordenadas: 1 antes que 2 antes que 3.
% Expected: SATISFIABLE
% ═══════════════════════════════════════════
#const bound=8.
#const hlim=3.

stack_base(b1; b2; b3).

% Patio inicialmente vacío; todos los containers llegan
arrive(1,1).
arrive(3,2).
arrive(2,3).
