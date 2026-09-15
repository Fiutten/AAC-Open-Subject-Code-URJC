# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT
"""Esqueleto CUDA con Numba. Requiere GPU NVIDIA y entorno CUDA compatible."""
import numpy as np
try:
    from numba import cuda
except ImportError:
    cuda=None

if cuda and cuda.is_available():
    @cuda.jit
    def suma(a,b,c):
        i=cuda.grid(1)
        if i<c.size: c[i]=a[i]+b[i]

    n=1_000_000
    a=np.ones(n,np.float32); b=np.ones(n,np.float32); c=np.empty_like(a)
    threads=256; blocks=(n+threads-1)//threads
    suma[blocks,threads](a,b,c)
    print(c[:5])
else:
    print("CUDA no disponible en este entorno; se conserva el ejemplo para un equipo compatible.")
