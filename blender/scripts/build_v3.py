"""Versión 3: piezas añadidas a partir de `docs/ficha-tecnica-piezas.md` (backlog P1–P4 de §8.3).

Orquesta los módulos por sistema. Se ejecuta desde `build_all.run(parts=(..., "v3", ...))`, antes de la
vista explosionada, y solo añade objetos a las colecciones de sistema ya existentes.
"""

import importlib
import sys

MODULES = ["ct_v3", "build_v3_estructura", "build_v3_exterior", "build_v3_chasis", "build_v3_motriz",
           "build_v3_interior", "build_v3_electronica", "build_v3_complemento"]


def _available():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    return [m for m in MODULES if os.path.exists(os.path.join(here, m + ".py"))]


def build_all(M):
    out = {}
    for name in _available():
        if name in sys.modules:
            importlib.reload(sys.modules[name])
    for name in _available():
        if name == "ct_v3":
            continue
        mod = importlib.import_module(name)
        objs = mod.build(M)
        out[name] = len(objs)
    return out
