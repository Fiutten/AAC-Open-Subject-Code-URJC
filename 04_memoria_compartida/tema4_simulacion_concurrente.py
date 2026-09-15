# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT
"""Solución orientativa para la práctica de concurrencia del Tema 4.

Modelo genérico de tres poblaciones sobre una rejilla compartida. El objetivo del
fichero es mostrar una solución reproducible a los requisitos de concurrencia:
un hilo por individuo, exclusión mutua, ocupación exclusiva de casillas,
prioridad atacar->mover, repoblación temporizada, generación periódica de una
población y una condición de terminación compartida.

No pretende fijar una única arquitectura de software ni sustituir la memoria
razonada del estudiante.
"""
from __future__ import annotations

from dataclasses import dataclass
import random
import threading
import time
from typing import Iterable


@dataclass(frozen=True)
class Pos:
    x: int
    y: int


class World:
    """Monitor del estado compartido de la simulación."""

    def __init__(self, size: int = 75, seed: int = 5):
        self.size = size
        self.rng = random.Random(seed)
        self.lock = threading.RLock()
        self.occupied: dict[tuple[int, int], Agent] = {}
        self.agents: list[Agent] = []
        self.finished = False
        self.winner: str | None = None
        self.queen_alive = True
        self.pending_b_respawns = 0
        self._seq = 0
        self._timers: list[threading.Timer] = []

    def next_name(self, prefix: str) -> str:
        with self.lock:
            self._seq += 1
            return f"{prefix}-{self._seq}"

    def free_position(self) -> Pos:
        """Devuelve una posición libre. Debe invocarse con el lock adquirido."""
        for _ in range(self.size * self.size * 2):
            p = (self.rng.randrange(self.size), self.rng.randrange(self.size))
            if p not in self.occupied:
                return Pos(*p)
        raise RuntimeError("No quedan casillas libres")

    def add_agent(self, agent: "Agent", start: bool = True) -> None:
        with self.lock:
            if self.finished:
                return
            pos = self.free_position()
            agent.pos = pos
            self.occupied[(pos.x, pos.y)] = agent
            self.agents.append(agent)
        if start:
            agent.start()

    def remove_from_map(self, agent: "Agent") -> None:
        self.occupied.pop((agent.pos.x, agent.pos.y), None)

    def alive_agents(self, faction: str | None = None) -> list["Agent"]:
        values = [a for a in self.occupied.values() if a.alive]
        return values if faction is None else [a for a in values if a.faction == faction]

    def adjacent_enemies(self, agent: "Agent") -> list["Agent"]:
        out: list[Agent] = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                other = self.occupied.get((agent.pos.x + dx, agent.pos.y + dy))
                if other and other.alive and other.faction != agent.faction:
                    out.append(other)
        return out

    def choose_target(self, agent: "Agent", enemies: Iterable["Agent"]) -> "Agent":
        enemies = list(enemies)
        # Ejemplo de prioridades. Pueden modificarse en una solución alternativa.
        if agent.faction == "B":
            order = ("Q", "A", "H")
        elif agent.faction in ("A", "Q"):
            order = ("B", "H")
        else:
            order = ("A", "Q", "B")
        for faction in order:
            candidates = [x for x in enemies if x.faction == faction]
            if candidates:
                return self.rng.choice(candidates)
        return self.rng.choice(enemies)

    def schedule(self, delay: float, callback) -> None:
        timer = threading.Timer(delay, callback)
        timer.daemon = True
        self._timers.append(timer)
        timer.start()

    def respawn_human(self) -> None:
        with self.lock:
            if self.finished:
                return
        self.add_agent(Human(self, self.next_name("H")))

    def respawn_b(self) -> None:
        with self.lock:
            if self.finished:
                self.pending_b_respawns = max(0, self.pending_b_respawns - 1)
                return
            self.pending_b_respawns = max(0, self.pending_b_respawns - 1)
        self.add_agent(HunterB(self, self.next_name("B")))

    def on_death(self, victim: "Agent") -> None:
        """Gestiona efectos de muerte y repoblación, siempre bajo RLock."""
        if victim.faction == "Q":
            self.queen_alive = False
        elif victim.faction == "H":
            self.schedule(0.35, self.respawn_human)
        elif victim.faction == "B":
            self.pending_b_respawns += 1
            self.schedule(5.0, self.respawn_b)

    def attack_or_move(self, agent: "Agent") -> None:
        with self.lock:
            if self.finished or not agent.alive:
                return

            enemies = self.adjacent_enemies(agent)
            if enemies:
                target = self.choose_target(agent, enemies)
                target.hp -= agent.damage
                print(f"{agent.name} ataca a {target.name} en {target.pos}")

                # Ejemplo de efecto adicional: atacar a A/Q puede causar daño de retorno a B.
                if agent.faction == "B" and target.faction in ("A", "Q"):
                    agent.hp -= 1

                if target.hp <= 0 and target.alive:
                    victim_pos = target.pos
                    target.alive = False
                    self.remove_from_map(target)
                    self.on_death(target)

                    # El atacante ocupa la casilla de la víctima si sigue vivo.
                    if agent.hp > 0:
                        self.remove_from_map(agent)
                        agent.pos = victim_pos
                        self.occupied[(victim_pos.x, victim_pos.y)] = agent
                    print(f"{target.name} muere; {agent.name} ocupa su casilla")

                if agent.hp <= 0 and agent.alive:
                    agent.alive = False
                    self.remove_from_map(agent)
                    self.on_death(agent)

                self.check_end()
                return

            free: list[Pos] = []
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    x, y = agent.pos.x + dx, agent.pos.y + dy
                    if 0 <= x < self.size and 0 <= y < self.size and (x, y) not in self.occupied:
                        free.append(Pos(x, y))
            if free:
                self.remove_from_map(agent)
                agent.pos = self.rng.choice(free)
                self.occupied[(agent.pos.x, agent.pos.y)] = agent

    def check_end(self) -> None:
        a_or_q = self.alive_agents("A") + self.alive_agents("Q")
        b = self.alive_agents("B")
        if not b and self.pending_b_respawns == 0:
            self.finished = True
            self.winner = "A"
        elif not self.queen_alive and not a_or_q:
            self.finished = True
            self.winner = "B"

    def stop(self) -> None:
        with self.lock:
            self.finished = True
        for timer in self._timers:
            timer.cancel()


class Agent(threading.Thread):
    def __init__(self, world: World, name: str, faction: str, hp: int, damage: int, delay: float):
        super().__init__(daemon=True, name=name)
        self.world = world
        self.agent_name = name
        self.faction = faction
        self.hp = hp
        self.damage = damage
        self.delay = delay
        self.pos = Pos(0, 0)
        self.alive = True

    @property
    def name(self) -> str:  # nombre legible usado también en las trazas
        return self.agent_name

    def run(self) -> None:
        while self.alive and not self.world.finished:
            self.world.attack_or_move(self)
            time.sleep(self.delay)


class SoldierA(Agent):
    def __init__(self, world: World, name: str):
        super().__init__(world, name, "A", hp=5, damage=4, delay=0.03)


class Queen(Agent):
    def __init__(self, world: World, name: str = "Q-0"):
        super().__init__(world, name, "Q", hp=100, damage=15, delay=0.05)


class HunterB(Agent):
    def __init__(self, world: World, name: str):
        super().__init__(world, name, "B", hp=20, damage=5, delay=0.05)


class Human(Agent):
    def __init__(self, world: World, name: str):
        super().__init__(world, name, "H", hp=3, damage=2, delay=0.08)


class QueenSpawner(threading.Thread):
    """Genera individuos A mientras la reina siga viva y no se alcance el máximo."""

    def __init__(self, world: World, maximum_a: int = 12, period: float = 30.0):
        super().__init__(daemon=True, name="queen-spawner")
        self.world = world
        self.maximum_a = maximum_a
        self.period = period

    def run(self) -> None:
        while not self.world.finished:
            time.sleep(self.period)
            with self.world.lock:
                if not self.world.queen_alive:
                    return
                count_a = len(self.world.alive_agents("A"))
            if count_a < self.maximum_a:
                self.world.add_agent(SoldierA(self.world, self.world.next_name("A")))


class Simulation:
    def __init__(self, size: int = 75):
        self.world = World(size=size)
        self.initial: list[Agent] = []
        self.spawner = QueenSpawner(self.world)

    def prepare(self) -> None:
        # Proporción inicial de ejemplo: 1 reina + 8 A, 3 B y 8 H.
        self.initial = [Queen(self.world)]
        self.initial += [SoldierA(self.world, f"A-{i}") for i in range(8)]
        self.initial += [HunterB(self.world, f"B-{i}") for i in range(3)]
        self.initial += [Human(self.world, f"H-{i}") for i in range(8)]
        for agent in self.initial:
            self.world.add_agent(agent, start=False)

    def run(self, seconds: float = 2.0) -> None:
        self.prepare()
        print("Posiciones iniciales (sin solapamientos):")
        with self.world.lock:
            for agent in self.initial:
                print(f"  {agent.name:5s} -> ({agent.pos.x:2d},{agent.pos.y:2d})")
        for agent in self.initial:
            agent.start()
        self.spawner.start()

        deadline = time.time() + seconds
        while time.time() < deadline and not self.world.finished:
            time.sleep(0.05)

        self.world.stop()
        for agent in list(self.world.agents):
            if agent.ident is not None:
                agent.join(timeout=0.2)
        self.spawner.join(timeout=0.2)
        print("Fin. Ganador:", self.world.winner or "sin decidir en el tiempo de demostración")


if __name__ == "__main__":
    Simulation(size=75).run(seconds=1.5)
