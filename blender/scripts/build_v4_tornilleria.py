"""Versión 4 · tornillería individual de las uniones atornilladas que no la tenían como pieza propia.

Cada juego de tornillos se crea como objeto aparte («<pieza>_Fasteners») que acompaña a su pieza en la vista
explosionada y se adelanta un poco más que ella, como en un despiece de taller. Cantidad, métrica (llave) y par
proceden de `docs/ficha-tecnica-piezas.md` (manual de servicio, [V]); la posición exacta de cada tornillo sobre
la pieza es una reconstrucción («Aproximado»).
"""

import math
from mathutils import Vector
import bpy
import ct_v4 as V4
from ct_v4 import screw, nut, torx, bolt
from build_v4_carroceria import bbox

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
NOTE = ("Cantidad, llave y par según el manual de servicio (docs/ficha-tecnica-piezas.md); posición de cada "
        "tornillo reconstruida")
# llave (mm) → diámetro nominal aproximado de la rosca (m)
THREAD = {7: 0.004, 8: 0.005, 10: 0.006, 13: 0.008, 15: 0.010, 18: 0.012, 21: 0.014, 24: 0.016}


def surface_z(name, x, y, below=0.0):
    """Altura de la cara superior de un objeto en (x, y) (rayo vertical descendente) menos el margen «below»."""
    from mathutils.bvhtree import BVHTree
    o = bpy.data.objects.get(name)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    tree = BVHTree.FromPolygons([mw @ v.co for v in me.vertices], [p.vertices[:] for p in me.polygons])
    ev.to_mesh_clear()
    hit = tree.ray_cast(Vector((x, y, 5.0)), Vector((0, 0, -1)))[0]
    return None if hit is None else hit.z - below


def _line(a, b, n):
    a, b = Vector(a), Vector(b)
    return [tuple(a + (b - a) * ((i + 0.5) / n)) for i in range(n)]


def fasteners(M, comp, pts, axis, label, key=10, head="flange", length=0.020, mat="zinc", extra=0.15):
    """Juego de tornillos de `comp` (misma explosión que la pieza, un poco más lejos)."""
    o = bpy.data.objects.get(comp)
    if o is None or not pts:
        return []
    d = THREAD.get(key, 0.006) if head != "torx" else key
    shapes = [screw(p, axis if not callable(axis) else axis(p), d, length, 0, head) for p in pts]
    edir = tuple(o.get("explode_dir", (0, 0, 1)))
    dist = float(o.get("explode_dist", 0.3)) + extra
    stage = int(o.get("explode_stage", 6))
    par = o.parent.name if o.parent is not None and o.parent.name != "CYBERTRUCK_ROOT" else None
    system = o.get("system", "BODY_FASTENERS")
    return V4.part(M, f"{comp}_Fasteners", system, [mat], shapes, label, parent=par, edir=edir, dist=dist,
                   stage=stage, group="Tornillería", fid="A", note=NOTE)


def build(M):
    out = []
    A = out.extend
    # Aletas delanteras: 3 pernos al pilar A + 2 a la viga superior (13 mm, 30 N·m) [EXT-013]
    for sd in ("FL", "FR"):
        bb = bbox(f"EXT_Fender_{sd}")
        if not bb:
            continue
        mn, mx = bb
        s = 1 if mx.x > 0 else -1
        xin = (mn.x if s > 0 else mx.x) + s * 0.035
        pil = _line((xin, mn.y + 0.035, mx.z - 0.04), (xin, mn.y + 0.035, mx.z - 0.30), 3)
        bm = _line((xin, mn.y + 0.30, mx.z - 0.012), (xin, mn.y + 0.75, mx.z - 0.012), 2)
        A(fasteners(M, f"EXT_Fender_{sd}", pil + bm, lambda p, s=s, mxz=mx.z: (-s, 0, 0) if p[2] < mxz - 0.02 else (0, 0, 1),
                    "Tornillos de la aleta delantera: 3 al pilar A y 2 a la viga superior (13 mm, 30 N·m)", 13))
    # Faros: 2 pernos de 10 mm a 5 N·m [EXT-110]
    for sd in ("L", "R"):
        bb = bbox(f"LGT_Headlamp_{sd}")
        if bb:
            mn, mx = bb
            A(fasteners(M, f"LGT_Headlamp_{sd}", _line((mn.x + 0.04, mn.y + 0.05, mx.z + 0.002),
                                                       (mx.x - 0.04, mn.y + 0.05, mx.z + 0.002), 2), Z,
                        "Tornillos del faro (2 × 10 mm, 5 N·m)", 10))
    # Retrovisores: 3 tornillos T40 de un solo uso a 18 N·m [EXT-054]
    for sd in ("L", "R"):
        bb = bbox(f"EXT_Mirror_{sd}_Arm")
        if bb:
            mn, mx = bb
            s = 1 if mx.x > 0 else -1
            xi = (mn.x if s > 0 else mx.x)
            c = Vector((xi, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
            pts = [tuple(c + Vector((0, 0.025 * math.cos(a), 0.025 * math.sin(a)))) for a in (0.5, 2.6, 4.7)]
            A(fasteners(M, f"EXT_Mirror_{sd}_Arm", pts, (-s, 0, 0),
                        "Tornillos del retrovisor (3 × T40 de un solo uso, 18 N·m; PN 1857466-00-B)", 0.008, "torx"))
    # Depósito del lavaparabrisas: 3 pernos de 10 mm a 8 N·m [EXT-107]
    bb = bbox("EXT_Washer_Tank")
    if bb:
        mn, mx = bb
        A(fasteners(M, "EXT_Washer_Tank", [(mn.x - 0.004, mn.y + 0.04, mx.z - 0.03), (mn.x - 0.004, mx.y - 0.04, mx.z - 0.03),
                                           (mn.x - 0.004, (mn.y + mx.y) / 2, mn.z + 0.05)], (-1, 0, 0),
                    "Tornillos del depósito del lavaparabrisas (3 × 10 mm, 8 N·m)", 10))
    # Motor del limpiaparabrisas: 3 pernos de 13 mm a 24 N·m [EXT-105]
    bb = bbox("EXT_Wiper_Motor")
    if bb:
        mn, mx = bb
        A(fasteners(M, "EXT_Wiper_Motor", _line((mn.x + 0.02, mn.y - 0.002, (mn.z + mx.z) / 2),
                                                (mx.x - 0.02, mn.y - 0.002, (mn.z + mx.z) / 2), 3), (0, -1, 0),
                    "Tornillos del motor del limpiaparabrisas (3 × 13 mm, 24 N·m)", 13))
    # Cubeta del frunk: 6 pernos de 10 mm a 12 N·m [EXT-066]
    bb = bbox("BODY_Frunk_Tub")
    if bb:
        mn, mx = bb
        # brida de apoyo 30 mm por debajo del borde real de la cubeta (queda bajo la tapa)
        xy = [(mn.x + 0.06 + (mx.x - mn.x - 0.12) * (i + 0.5) / 4, mx.y - 0.05) for i in range(4)]
        xy += [(mn.x + 0.05, (mn.y + mx.y) / 2), (mx.x - 0.05, (mn.y + mx.y) / 2)]
        pts = [(x, y, surface_z("BODY_Frunk_Tub", x, y, 0.030)) for x, y in xy]
        pts = [p for p in pts if p[2] is not None]
        A(fasteners(M, "BODY_Frunk_Tub", pts, Z, "Tornillos de la cubeta del frunk (6 × 10 mm, 12 N·m)", 10))
    # Raíles de la cubierta: 9 pernos de 10 mm a 9 N·m por lado [EXT-092]
    for sd in ("L", "R"):
        bb = bbox(f"CARGO_Tonneau_Rail_{sd}")
        if bb:
            mn, mx = bb
            s = 1 if mx.x > 0 else -1
            xi = (mn.x if s > 0 else mx.x) - s * 0.002
            zc = (mn.z + mx.z) / 2
            A(fasteners(M, f"CARGO_Tonneau_Rail_{sd}", _line((xi, mn.y + 0.05, zc), (xi, mx.y - 0.05, zc), 9),
                        (-s, 0, 0), "Tornillos del raíl de la cubierta (9 × 10 mm, 9 N·m)", 10))
    # Suelo de la caja: 12 pernos cortos de 15 mm a 56 N·m y 2 largos a 46 N·m [EXT-073]
    bb = bbox("CARGO_Bed_Tub")
    if bb:
        mn, mx = bb
        zf = 0.866
        pts = _line((mn.x + 0.06, mn.y + 0.10, zf), (mn.x + 0.06, mx.y - 0.10, zf), 6)
        pts += _line((mx.x - 0.06, mn.y + 0.10, zf), (mx.x - 0.06, mx.y - 0.10, zf), 6)
        pts += [(-0.10, mx.y - 0.08, zf), (0.10, mx.y - 0.08, zf)]
        A(fasteners(M, "CARGO_Bed_Tub", pts, Z, "Tornillos del suelo de la caja (12 cortos de 15 mm a 56 N·m y 2 "
                                                "largos a 46 N·m)", 15, length=0.030))
    # Luz del portón: 8 tornillos T30 a 5 N·m [EXT-113]
    bb = bbox("LGT_Rear_Lightbar_Housing")
    if bb:
        mn, mx = bb
        A(fasteners(M, "LGT_Rear_Lightbar_Housing", _line((mn.x + 0.05, mx.y + 0.002, (mn.z + mx.z) / 2),
                                                          (mx.x - 0.05, mx.y + 0.002, (mn.z + mx.z) / 2), 8), Y,
                    "Tornillos de la luz del portón (8 × T30, 5 N·m)", 0.005, "torx"))
    # Pilotos laterales de la caja: 2 tornillos T30 a 5 N·m [EXT-112]
    for sd in ("L", "R"):
        bb = bbox(f"LGT_TailLamp_BodySide_{sd}")
        if bb:
            mn, mx = bb
            s = 1 if mx.x > 0 else -1
            xi = (mn.x if s > 0 else mx.x) - s * 0.002
            A(fasteners(M, f"LGT_TailLamp_BodySide_{sd}", _line((xi, (mn.y + mx.y) / 2, mn.z + 0.01),
                                                                (xi, (mn.y + mx.y) / 2, mx.z - 0.01), 2), (-s, 0, 0),
                        "Tornillos del piloto lateral (2 × T30, 5 N·m)", 0.005, "torx"))
    # Fascia trasera: 2 pernos centrales de 10 mm y 9 del difusor a 6 N·m [EXT-017]
    bb = bbox("EXT_Rear_Diffuser")
    if bb:
        mn, mx = bb
        pts = _line((mn.x + 0.08, (mn.y + mx.y) / 2, mn.z - 0.002), (mx.x - 0.08, (mn.y + mx.y) / 2, mn.z - 0.002), 9)
        A(fasteners(M, "EXT_Rear_Diffuser", pts, (0, 0, -1), "Tornillos del difusor (9 × 10 mm, 6 N·m)", 10))
    bb = bbox("EXT_Rear_Bumper")
    if bb:
        mn, mx = bb
        A(fasteners(M, "EXT_Rear_Bumper", [(-0.06, mn.y + 0.06, mx.z - 0.030), (0.06, mn.y + 0.06, mx.z - 0.030)],
                    Z, "Tornillos centrales de la fascia trasera (2 × 10 mm, 6 N·m)", 10))
    # Fascia delantera: 4 pernos de 10 mm a 4 N·m y 1 lateral por lado a 6 N·m [EXT-001]
    bb = bbox("EXT_Front_Bumper")
    if bb:
        mn, mx = bb
        zc = (mn.z + mx.z) / 2
        pts = _line((mn.x + 0.25, mn.y - 0.002, zc), (mx.x - 0.25, mn.y - 0.002, zc), 4)
        A(fasteners(M, "EXT_Front_Bumper", pts, (0, -1, 0), "Tornillos de la fascia delantera (4 × 10 mm, 4 N·m)", 10))
    # Barra de luz: 2 tuercas a 3 N·m y 2 pernos a 4 N·m (10 mm) [EXT-111]
    bb = bbox("LGT_Front_Lightbar_Housing")
    if bb:
        mn, mx = bb
        A(fasteners(M, "LGT_Front_Lightbar_Housing", _line((mn.x + 0.10, mn.y - 0.002, (mn.z + mx.z) / 2),
                                                           (mx.x - 0.10, mn.y - 0.002, (mn.z + mx.z) / 2), 4), (0, -1, 0),
                    "Fijaciones de la barra de luz (2 tuercas a 3 N·m y 2 pernos a 4 N·m, 10 mm)", 10))
    # Unidades motrices: tornillos de los soportes elásticos al subchasis (A: cantidad no publicada)
    for du in ("DU_F_Mounts", "DU_R_Mounts"):
        o = bpy.data.objects.get(du)
        if o is None:
            continue
        bb = bbox(du)
        mn, mx = bb
        pts = []
        for p in ((mn.x + 0.04, (mn.y + mx.y) / 2, mn.z + 0.004), (mx.x - 0.04, (mn.y + mx.y) / 2, mn.z + 0.004),
                  ((mn.x + mx.x) / 2, mx.y - 0.04, mn.z + 0.004)):
            pts += [(p[0] - 0.025, p[1], p[2]), (p[0] + 0.025, p[1], p[2])]
        A(fasteners(M, du, pts, (0, 0, -1), "Tornillos de los soportes de la unidad motriz al subchasis (18 mm)", 18,
                    length=0.040))
    return out
