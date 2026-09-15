# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT
"""Ejemplo mínimo de composición de tareas con Parsl."""
try:
    import parsl
    from parsl import python_app
except ImportError:
    parsl=None

if parsl:
    parsl.load()
    @python_app
    def cuadrado(x): return x*x
    @python_app
    def suma(a,b): return a+b
    a=cuadrado(3); b=cuadrado(4)
    print(suma(a,b).result())
else:
    print("Instale Parsl para ejecutar este ejemplo: pip install parsl")
