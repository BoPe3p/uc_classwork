"""
Container Bay Visualizer — C-PMP (D1-D4)

Uso:
    python visualizer.py pauta_d3.lp tests/D3/d3_test2.lp [salida.html]
    python visualizer.py pauta_d4.lp tests/D4/d4_test1.lp

Flags:
    --bound N     Usar bound fijo N (por defecto: búsqueda automática desde 1)
    --max-bound N Límite máximo para la búsqueda automática (default: 40)
    --timeout N   Tiempo máximo por intento en segundos (default: 60)

El bound automático prueba 1, 2, 3... hasta encontrar la primera solución
satisfacible, ignorando el #const bound del archivo de test.
"""

import re
import sys
import json
import subprocess
import os
import tempfile

RE_ON         = re.compile(r'\bon\((\w+),(\w+),(\d+)\)')
RE_MOVE       = re.compile(r'\bmove\((\w+),(\w+),(\d+)\)')
RE_DROP       = re.compile(r'\bdrop\((\w+),(\w+),(\d+)\)')
RE_STACK_BASE = re.compile(r'\bstack_base\((\w+)\)')
RE_CONTAINER  = re.compile(r'\bcontainer\((\w+)\)')
RE_AVAILABLE  = re.compile(r'\bavailable\((\w+),(\d+)\)')
RE_ARRIVE     = re.compile(r'\barrive\((\w+),(\d+)\)')

# Added to every clingo run to expose needed atoms regardless of #show in pauta
SHOW_EXTRA = """\
#show on/3.
#show move/3.
#show drop/3.
#show stack_base/1.
#show container/1.
#show available/2.
#show arrive/2.
"""


def extract_last_model(output: str) -> str:
    lines = output.splitlines()
    indices = [i for i, l in enumerate(lines) if l.startswith('Answer:')]
    if not indices:
        return output
    last = indices[-1]
    parts = []
    for i in range(last + 1, len(lines)):
        line = lines[i].strip()
        if not line or line.startswith(('Optimization:', 'SATISFIABLE', 'OPTIMUM FOUND', 'UNSATISFIABLE')):
            break
        parts.append(line)
    return ' '.join(parts)


def _try_clingo(cmd: list, time_limit: int) -> tuple[str, bool]:
    """Ejecuta clingo y devuelve (stdout, timeout_occurred)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=time_limit)
        if result.returncode not in (0, 10, 20, 30):
            raise RuntimeError(f"Clingo error ({result.returncode}): {result.stderr.strip()}")
        return result.stdout, False
    except subprocess.TimeoutExpired:
        return '', True


RE_CONST_BOUND = re.compile(r'#const\s+bound\s*=\s*(\d+)')


def read_bound_from_files(asp_files: list) -> int | None:
    """Lee el #const bound=N declarado en cualquiera de los archivos .lp."""
    for path in asp_files:
        try:
            with open(path, encoding='utf-8') as f:
                content = f.read()
            m = RE_CONST_BOUND.search(content)
            if m:
                return int(m.group(1))
        except OSError:
            pass
    return None


def run_clingo(asp_files: list, time_limit: int = 60,
               fixed_bound: int | None = None, max_bound: int = 40) -> str | None:
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.lp', delete=False, encoding='utf-8')
    tmp.write(SHOW_EXTRA)
    tmp.close()

    try:
        if fixed_bound is not None:
            bounds = [fixed_bound]
            print(f"🔍 Buscando solución con bound={fixed_bound}...")
        else:
            # Respetar el #const bound=N del archivo de test como mínimo.
            file_bound = read_bound_from_files(asp_files)
            start = file_bound if file_bound is not None else 1
            if file_bound is not None:
                print(f"🔍 Buscando bound mínimo desde {start} (según #const bound={file_bound} en los archivos)...")
            else:
                print(f"🔍 Buscando bound mínimo (1..{max_bound})...")
            bounds = range(start, max_bound + 1)

        for b in bounds:
            # -c bound=N sobreescribe cualquier #const bound en los archivos .lp
            cmd = ['clingo', *asp_files, tmp.name, '-c', f'bound={b}']

            stdout, timed_out = _try_clingo(cmd, time_limit)

            if timed_out:
                print(f"   bound={b}: tiempo agotado ({time_limit}s)")
                if fixed_bound is not None:
                    print("   Usa --timeout N para aumentar el límite.")
                    return None
                continue

            if 'UNSATISFIABLE' in stdout:
                if fixed_bound is None:
                    print(f"   bound={b}: sin solución")
                continue

            if 'SATISFIABLE' in stdout or 'OPTIMUM FOUND' in stdout:
                tag = '✓ óptimo' if 'OPTIMUM FOUND' in stdout else '✓ satisfacible'
                print(f"   bound={b}: {tag}")
                return extract_last_model(stdout)

        print(f"❌ No se encontró solución con bound ≤ {max_bound}.")
        print("   Aumenta --max-bound N o revisa el problema.")
        return None

    except FileNotFoundError:
        print("❌ Clingo no encontrado. Instala con: brew install clingo")
        sys.exit(1)
    finally:
        os.unlink(tmp.name)


def compute_positions(on_map: dict, stack_bases: set) -> dict:
    """
    Convierte on/3 en un timestep a posiciones {container: {pila, altura}}.
    on_map: {C1: C2} donde C1 está sobre C2.
    """
    positions = {}
    # Build reverse map for quick lookup: C2 -> C1 (what's on top of C2)
    above = {}
    for c1, c2 in on_map.items():
        above[c2] = c1

    for base in stack_bases:
        height = 1
        current = base
        while current in above:
            c = above[current]
            positions[c] = {"pila": base, "altura": height}
            current = c
            height += 1
    return positions


def parse_model(text: str) -> dict | None:
    on_tuples    = [(m.group(1), m.group(2), int(m.group(3))) for m in RE_ON.finditer(text)]
    move_tuples  = [(m.group(1), m.group(2), int(m.group(3))) for m in RE_MOVE.finditer(text)]
    drop_tuples  = [(m.group(1), m.group(2), int(m.group(3))) for m in RE_DROP.finditer(text)]
    stack_bases  = sorted(m.group(1) for m in RE_STACK_BASE.finditer(text))
    containers   = set(m.group(1) for m in RE_CONTAINER.finditer(text))
    arrive_list  = [(m.group(1), int(m.group(2))) for m in RE_ARRIVE.finditer(text)]

    available_at: dict[int, list] = {}
    for m in RE_AVAILABLE.finditer(text):
        available_at.setdefault(int(m.group(2)), []).append(m.group(1))

    if not on_tuples or not stack_bases:
        return None

    # Group on/3 by timestep
    on_at: dict[int, dict] = {}
    for c1, c2, t in on_tuples:
        on_at.setdefault(t, {})[c1] = c2

    times = sorted(on_at.keys())

    # Precompute positions per timestep
    pos_at = {t: compute_positions(on_at[t], set(stack_bases)) for t in times}

    # hlim = max height seen across all timesteps
    hlim = max(
        (p["altura"] for positions in pos_at.values() for p in positions.values()),
        default=1
    )

    # arrive_time: {container: arrival_time}
    arrive_time = dict(arrive_list)

    # Build action_at[T+1] from move/3 and drop/3 at T
    action_at: dict[int, dict] = {}

    for c1, c2, t in move_tuples:
        if t + 1 not in times:
            continue
        src = pos_at.get(t, {}).get(c1)
        if c2 in stack_bases:
            dest_pila = c2
        else:
            dest = pos_at.get(t, {}).get(c2)
            dest_pila = dest["pila"] if dest else None
        action_at[t + 1] = {
            "tipo": "move",
            "contenedor": c1,
            "origen": src["pila"] if src else None,
            "destino": dest_pila,
        }

    for c1, c2, t in drop_tuples:
        if t + 1 not in times:
            continue
        if c2 in stack_bases:
            dest_pila = c2
        else:
            dest = pos_at.get(t, {}).get(c2)
            dest_pila = dest["pila"] if dest else None
        action_at[t + 1] = {
            "tipo": "drop",
            "contenedor": c1,
            "destino": dest_pila,
        }

    has_arrivals = bool(drop_tuples) or bool(arrive_list)

    pasos = []
    for t in times:
        pendientes = [
            [c, ta] for c, ta in sorted(arrive_time.items(), key=lambda x: x[1])
            if ta > t
        ]
        pasos.append({
            "t": t,
            "posiciones": pos_at[t],
            "accion": action_at.get(t),
            "disponibles": sorted(available_at.get(t, []), key=lambda c: arrive_time.get(c, 0)),
            "pendientes": pendientes,
        })

    prioridades = {}
    for c in containers:
        try:
            prioridades[c] = int(c)
        except ValueError:
            prioridades[c] = 0

    return {
        "config": {
            "pilas": stack_bases,
            "altura_max": hlim,
            "modo": "C-PMP+D4" if has_arrivals else "C-PMP",
        },
        "prioridades": prioridades,
        "pasos": pasos,
    }


def generate_html(data: dict, template_path: str, output_path: str):
    with open(template_path, encoding='utf-8') as f:
        template = f.read()
    output = template.replace('"__DATA_PLACEHOLDER__"', json.dumps(data, ensure_ascii=False))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)


def main():
    time_limit = 60
    max_bound  = 40
    fixed_bound = None
    asp_files = []
    out_file = 'visualizacion.html'

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--timeout' and i + 1 < len(args):
            time_limit = int(args[i + 1]); i += 1
        elif args[i] == '--bound' and i + 1 < len(args):
            fixed_bound = int(args[i + 1]); i += 1
        elif args[i] == '--max-bound' and i + 1 < len(args):
            max_bound = int(args[i + 1]); i += 1
        elif args[i].endswith('.lp'):
            asp_files.append(args[i])
        elif args[i].endswith('.html'):
            out_file = args[i]
        i += 1

    if not asp_files:
        print("Uso: python visualizer.py pauta_dN.lp tests/DN/test.lp [salida.html]")
        print()
        print("Flags:")
        print("  --bound N       Usar bound fijo (sin búsqueda automática)")
        print("  --max-bound N   Límite de la búsqueda automática (default: 40)")
        print("  --timeout N     Segundos por intento (default: 60)")
        print()
        print("Ejemplos:")
        print("  python visualizer.py pauta_d3.lp tests/D3/d3_test2.lp")
        print("  python visualizer.py pauta_d4.lp tests/D4/d4_test1.lp")
        sys.exit(1)

    print("╔══════════════════════════════════════╗")
    print("║    Container Bay Visualizer — C-PMP  ║")
    print("╚══════════════════════════════════════╝")
    print(f"  Archivos: {', '.join(asp_files)}")
    if fixed_bound is not None:
        print(f"  Bound:    {fixed_bound} (fijo)")
    else:
        print(f"  Bound:    automático (máx {max_bound})")
    print()

    model_text = run_clingo(asp_files, time_limit, fixed_bound, max_bound)
    if model_text is None:
        sys.exit(1)

    data = parse_model(model_text)
    if data is None:
        print("❌ No se encontraron átomos on/3 o stack_base/1 en el modelo.")
        print("   Verifica que tu programa incluya la regla de inercia y el input correcto.")
        sys.exit(1)

    cfg = data['config']
    print(f"  📊 Contenedores: {len(data['prioridades'])}")
    print(f"  📚 Pilas: {len(cfg['pilas'])}  hlim={cfg['altura_max']}")
    print(f"  🕐 Pasos: {len(data['pasos'])}")
    print(f"  🏷️  Modo: {cfg['modo']}")
    print()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'template.html')
    if not os.path.exists(template_path):
        print(f"❌ template.html no encontrado en {script_dir}")
        sys.exit(1)

    generate_html(data, template_path, out_file)
    print(f"  ✅ Generado: {out_file}")
    print(f"     Ábrelo en tu navegador.")


if __name__ == '__main__':
    main()
