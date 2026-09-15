# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from typing import Optional

STAGES = ("IF", "ID", "EX", "MEM", "WB")

@dataclass
class Instruction:
    text: str
    op: str
    dst: Optional[str]
    src: tuple[str, ...]
    is_load: bool = False
    is_branch: bool = False


def parse(line: str) -> Instruction:
    clean = line.replace(",", " ").replace("(", " ").replace(")", " ")
    p = clean.split()
    op = p[0].upper()
    if op in {"ADD", "SUB", "AND", "OR"}:
        return Instruction(line, op, p[1], (p[2], p[3]))
    if op == "ADDI":
        return Instruction(line, op, p[1], (p[2],))
    if op == "LW":
        # LW Rt offset(Rs)
        return Instruction(line, op, p[1], (p[3],), is_load=True)
    if op == "SW":
        return Instruction(line, op, None, (p[1], p[3]))
    if op in {"BEQ", "BNE"}:
        return Instruction(line, op, None, (p[1], p[2]), is_branch=True)
    if op == "J":
        return Instruction(line, op, None, (), is_branch=True)
    raise ValueError(f"Operación no soportada: {op}")


def simulate(lines: list[str]) -> None:
    program = [parse(x.strip()) for x in lines if x.strip() and not x.strip().startswith("#")]
    pipe: list[Optional[int]] = [None] * 5
    pc = 0
    cycle = 0
    completed = 0
    trace = []

    def inst_at(slot):
        return program[slot] if slot is not None else None

    while completed < len(program):
        cycle += 1
        # WB completes
        if pipe[4] is not None:
            completed += 1

        # Load-use hazard: an instruction in ID consumes the result of a load currently in EX.
        stall = False
        id_i = inst_at(pipe[1])
        ex_i = inst_at(pipe[2])
        if id_i and ex_i and ex_i.is_load and ex_i.dst and ex_i.dst in id_i.src:
            stall = True

        old = pipe[:]
        if stall:
            # WB <- MEM, MEM <- EX; insert bubble in EX; keep ID and IF.
            pipe[4] = old[3]
            pipe[3] = old[2]
            pipe[2] = None
            pipe[1] = old[1]
            pipe[0] = old[0]
        else:
            pipe[4] = old[3]
            pipe[3] = old[2]
            pipe[2] = old[1]
            pipe[1] = old[0]
            pipe[0] = pc if pc < len(program) else None
            if pc < len(program):
                pc += 1

        # The exercise resolves branches in ID. In this compact reference model we do not
        # evaluate register values; a branch is shown as a control point where a real simulator
        # would select/flush the next PC.
        branch_note = ""
        if pipe[1] is not None and program[pipe[1]].is_branch:
            branch_note = " [salto resuelto en ID: evaluar condición/objetivo]"

        row = []
        for s, idx in zip(STAGES, pipe):
            row.append(f"{s}: {program[idx].text}" if idx is not None else f"{s}: --")
        trace.append((cycle, stall, branch_note, row))

    for cycle, stall, branch_note, row in trace:
        print(f"Ciclo {cycle:02d}" + ("  STALL(load-use)" if stall else "") + branch_note)
        print(" | ".join(row))


if __name__ == "__main__":
    sample = [
        "LW R1, 0(R2)",
        "ADD R3, R1, R4",   # load-use: requiere una burbuja aun con forwarding
        "SUB R5, R3, R6",   # RAW resoluble por forwarding EX/MEM -> EX
        "SW R5, 4(R2)",
        "BEQ R5, R0, fin",
        "OR R7, R3, R5",
    ]
    simulate(sample)
