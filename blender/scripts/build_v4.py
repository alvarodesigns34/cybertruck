"""Versión 4 («coche completo»): interior funcional de los conjuntos, tornillería y piezas que faltaban.

Orquesta los módulos `build_v4_*.py`. Se ejecuta desde `build_all.run(parts=(..., "v3", "v4", ...))`,
después de la versión 3 y antes de la vista explosionada; solo añade objetos a las colecciones de sistema
existentes y ajusta la explosión de algunas carcasas para que se aparten más que su contenido.
"""

import importlib
import sys

MODULES = ["ct_v4", "build_v4_motriz", "build_v4_chasis", "build_v4_energia", "build_v4_habitaculo",
           "build_v4_carroceria", "build_v4_tornilleria"]


def _available():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    return [m for m in MODULES if os.path.exists(os.path.join(here, m + ".py"))]


def build_all(M, only=None):
    import bpy
    out = {}
    # las piezas de la v4 se describen a menudo en las coordenadas de objetos ya creados: hay que
    # actualizar las matrices de mundo antes de leerlas
    bpy.context.view_layer.update()
    for name in _available():
        if name in sys.modules:
            importlib.reload(sys.modules[name])
    for name in _available():
        if name == "ct_v4" or (only and name not in only):
            continue
        mod = importlib.import_module(name)
        objs = mod.build(M)
        out[name] = len(objs)
    return out
