#!/usr/bin/env python3
"""Validación estructural de la colección pública de código docente."""

from __future__ import annotations

import json
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "__pycache__"}


def visible(path: Path) -> bool:
    return not any(part in EXCLUDED for part in path.parts)


def main() -> None:
    py_files = sorted(path for path in ROOT.rglob("*.py") if visible(path))
    notebooks = sorted(path for path in ROOT.rglob("*.ipynb") if visible(path))

    if not py_files:
        raise RuntimeError("No se han encontrado programas Python.")

    for path in py_files:
        if path == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8")
        if "SPDX-License-Identifier: MIT" not in text:
            raise RuntimeError(f"Falta el encabezado SPDX: {path.relative_to(ROOT)}")
        py_compile.compile(str(path), doraise=True)

    for path in notebooks:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        metadata = notebook.get("metadata", {}).get("aac_publication", {})
        expected = {
            "author": "Alberto Fernández Isabel",
            "license": "MIT",
            "course": "2026-2027",
        }
        if metadata != expected:
            raise RuntimeError(
                f"Metadatos de publicación incorrectos: {path.relative_to(ROOT)}"
            )
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") == "code" and cell.get("outputs"):
                raise RuntimeError(
                    f"El notebook contiene salidas: {path.relative_to(ROOT)}"
                )

    print(
        f"Validación correcta: {len(py_files) - 1} programas y "
        f"{len(notebooks)} notebooks."
    )


if __name__ == "__main__":
    main()
