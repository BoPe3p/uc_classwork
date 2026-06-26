% ═══════════════════════════════════════════
% D2 Test 4: Mover sobre un container tapado (inválido)
% Container 4 tiene a 2 encima. Mover algo sobre 4 es inválido.
% Expected: UNSATISFIABLE
% ═══════════════════════════════════════════
#const bound=1.

stack_base(b1; b2).
container(1..4).

on(4,b1,0).
on(2,4,0).   % 2 sobre 4: 4 no está libre
on(1,b2,0).
on(3,1,0).

% Intentar poner 3 sobre 4 (que está tapado por 2): inválido
move(3,4,0).
