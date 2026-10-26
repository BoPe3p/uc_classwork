import sys
import time
import numpy as np
from numba import njit
from mpi4py import MPI

G = 1.0
EPS = 0.1  # suavizado: evita fuerzas muy grandes cuando dos particulas se acercan
dt = 5e-3

# Comunicadores
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Tenemos que repartir los cuerpos
def repartir(n, size):
    base = n // size
    resto = n % size
    # el rank r recibe base + 1 si r < resto, y base si no.
    counts = [base + 1 if r < resto else base for r in range(size)]
    starts = [0] * size
    for r in range(1, size):
        starts[r] = starts[r - 1] + counts[r - 1]
    return counts, starts

# Calculamos las aceleraciones por bloques [i0, i1)
# i = indices de los cuerpos que calculamos la acc
# j = resto de cuerpos que tienen efecto en i
@njit
def aceleraciones(pos, m, i0, i1):
    largo = i1-i0
    n = pos.shape[0]
    acc = np.zeros((largo, 2))
    for i in range(i0, i1):
        for j in range(n):
            if j != i:
                dx = pos[j, 0] - pos[i, 0]
                dy = pos[j, 1] - pos[i, 1]
                r2 = dx * dx + dy * dy + EPS * EPS
                f = G * m[j] / (r2 * np.sqrt(r2))
                acc[i-i0, 0] += f * dx
                acc[i-i0, 1] += f * dy
    return acc

@njit
def energia(pos, vel, m, i0, i1):
    largo = i1-i0
    n = pos.shape[0]
    e = 0.0
    for i in range(i0, i1):
        e += 0.5 * m[i] * (vel[i, 0] ** 2 + vel[i, 1] ** 2)
        for j in range(n):
            if j != i:
                dx = pos[j, 0] - pos[i, 0]
                dy = pos[j, 1] - pos[i, 1]
                e -= 0.5 * G * m[i] * m[j] / np.sqrt(dx * dx + dy * dy + EPS * EPS)
    return e

def energia_total(e_loc):
    if rank == 0:
        total = e_loc
        for r in range(1, size):
            total += comm.recv(source=r, tag=1)
        return total
    comm.send(e_loc, dest=0, tag=1)
    return None

def intercambiar_posiciones(pos, counts, starts):
    for r in range(size):
        s, c = starts[r], counts[r]
        if rank == r:
            for dest in range(size):
                if dest != rank:
                    comm.Send(pos[s:s + c], dest=dest, tag=0)
        else:
            comm.Recv(pos[s:s + c], source=r, tag=0)   # escribe directo en pos

def galaxia(n, centro, velocidad, rng):
    r = 0.2 + 0.8 * rng.random(n)
    theta = 2 * np.pi * rng.random(n)
    v = np.sqrt(G / r)
    pos = np.column_stack((r * np.cos(theta), r * np.sin(theta)))
    vel = np.column_stack((-v * np.sin(theta), v * np.cos(theta)))
    pos[0] = 0.0
    vel[0] = 0.0
    m = np.full(n, 0.1 / n)
    m[0] = 1.0
    return pos + centro, vel + velocidad, m


def condicion_inicial(n):
    rng = np.random.default_rng(0)
    pos1, vel1, m1 = galaxia(n // 2, [-2.0, -0.7], [0.25, 0.0], rng)
    pos2, vel2, m2 = galaxia(n - n // 2, [2.0, 0.7], [-0.25, 0.0], rng)
    return np.vstack((pos1, pos2)), np.vstack((vel1, vel2)), np.concatenate((m1, m2))


def simular(pos, vel, m, pasos, cada, counts, starts):
    i0, i1 = starts[rank], starts[rank] + counts[rank]
    frames = []
    acc = aceleraciones(pos, m, i0, i1)
    for k in range(pasos):
        vel[i0:i1] += 0.5 * dt * acc
        pos[i0:i1] += dt * vel[i0:i1]
        intercambiar_posiciones(pos, counts, starts)   # pos completo y actualizado
        acc = aceleraciones(pos, m, i0, i1)
        vel[i0:i1] += 0.5 * dt * acc
        if rank == 0 and k % cada == 0:
            frames.append(pos.copy())
    e = energia_total(energia(pos, vel, m, i0, i1))
    return e, frames


if __name__ == "__main__":
    n = int(sys.argv[1])
    pasos = int(sys.argv[2])

    pos, vel, m = condicion_inicial(n)       # igual en todos los ranks (seed fija)
    counts, starts = repartir(n, size)
    i0, i1 = starts[rank], starts[rank] + counts[rank]

    aceleraciones(pos, m, i0, i1)            # warm-up de numba
    e0 = energia_total(energia(pos, vel, m, i0, i1))

    t0 = time.perf_counter()
    e, frames = simular(pos, vel, m, pasos, 20, counts, starts)
    elapsed = time.perf_counter() - t0

    if rank == 0:
        np.save("frames.npy", np.array(frames))
        print(f"p={size}, n={n}, pasos={pasos}, dE/E={abs((e - e0) / e0):.2e}, tiempo={elapsed:.4f}")
