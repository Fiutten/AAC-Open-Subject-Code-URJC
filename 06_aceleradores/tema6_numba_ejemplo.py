# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT

import time
import numpy as np

try:
    from numba import njit
except ImportError:
    njit = None


def suma_cuadrados_py(a):
    s = 0.0
    for x in a:
        s += x * x
    return s

if njit:
    suma_cuadrados_jit = njit(suma_cuadrados_py)
else:
    suma_cuadrados_jit = None

if __name__ == '__main__':
    a = np.arange(1_000_000, dtype=np.float64)
    t0=time.perf_counter(); r1=suma_cuadrados_py(a); t1=time.perf_counter()-t0
    print('Python:', t1, r1)
    if suma_cuadrados_jit:
        suma_cuadrados_jit(a)  # primera llamada: compila
        t0=time.perf_counter(); r2=suma_cuadrados_jit(a); t2=time.perf_counter()-t0
        print('Numba:', t2, r2)
    else:
        print('Numba no instalado; el ejemplo sigue siendo válido como material de referencia.')
