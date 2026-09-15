# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT

class Recurso:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.activo = True

    def descripcion(self):
        return f"{self.nombre}: capacidad={self.capacidad}, activo={self.activo}"


class Procesador(Recurso):
    def __init__(self, nombre, capacidad, nucleos):
        super().__init__(nombre, capacidad)
        self.nucleos = nucleos
        self.tareas = []

    def asignar(self, tarea):
        if len(self.tareas) < self.nucleos:
            self.tareas.append(tarea)
            return True
        return False


class Tarea:
    def __init__(self, nombre, coste):
        self.nombre = nombre
        self.coste = coste

    def __repr__(self):
        return f"Tarea({self.nombre!r}, coste={self.coste})"


class Sistema:
    def __init__(self):
        self.recursos = []

    def agregar(self, recurso):
        self.recursos.append(recurso)

    def buscar(self, nombre):
        for recurso in self.recursos:
            if recurso.nombre == nombre:
                return recurso
        return None
