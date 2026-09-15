# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT

import random
import time

N = 2_000_000


def predecible(datos):
    s = 0
    for x in datos:
        if x >= 0:          # casi siempre la misma dirección
            s += x
        else:
            s -= x
    return s


def impredecible(datos):
    s = 0
    for x in datos:
        if x & 1:           # patrón menos predecible
            s += x
        else:
            s -= x
    return s


def medir(fn, datos):
    t0 = time.perf_counter()
    resultado = fn(datos)
    return time.perf_counter() - t0, resultado


if __name__ == "__main__":
    rng = random.Random(7)
    positivos = [rng.randrange(0, 100) for _ in range(N)]
    mezcla = [rng.randrange(0, 100) for _ in range(N)]
    for fn, datos in [(predecible, positivos), (impredecible, mezcla)]:
        dt, r = medir(fn, datos)
        print(fn.__name__, f"{dt:.6f}s", r)
    print("Interpretar los tiempos con cautela: Python, el intérprete, la caché y el SO añaden ruido.")
