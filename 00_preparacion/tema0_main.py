# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT

from tema0_modelo import Procesador, Recurso, Sistema, Tarea


def main():
    sistema = Sistema()
    sistema.agregar(Procesador("CPU-0", 100, 2))
    sistema.agregar(Recurso("RAM", 32))

    tareas = [Tarea("A", 10), Tarea("B", 20), Tarea("C", 5)]
    cpu = sistema.buscar("CPU-0")

    i = 0
    while i < len(tareas):
        tarea = tareas[i]
        if cpu.asignar(tarea):
            print("Asignada:", tarea)
        else:
            print("Sin hueco para:", tarea)
        i += 1

    for recurso in sistema.recursos:
        print(recurso.descripcion())


if __name__ == "__main__":
    main()
